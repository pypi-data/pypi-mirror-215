# Copyright © 2022 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: BSD-3-Clause

"""Utilities to needed to release packages."""

from __future__ import annotations

import difflib
import logging
import re
import time

from distutils.version import StrictVersion

import gitlab
import gitlab.v4.objects
import packaging.version
import tomlkit

from git import Repo
from pkg_resources import Requirement

from idiap_devtools.profile import Profile

logger = logging.getLogger(__name__)


def _update_readme(
    contents: str,
    version: str,
    default_branch: str,
) -> str:
    """Updates README file text to make it release/latest ready.

    Inside text of the readme, replaces parts of the links to the provided
    version. If version is not provided, replace to `stable` or the default
    project branch name.

    Arguments:

        context: Text of the README.rst file from a package

        version: Format of the version string is '#.#.#'

        default_branch: The name of the default project branch to use

    Returns:

        New text of readme with all replaces done
    """

    variants = {
        "available",
        "latest",
        "main",
        "master",
        "stable",
        default_branch,
        packaging.version.VERSION_PATTERN,
    }

    # matches the graphical badge in the readme's text with the given version
    DOC_IMAGE = re.compile(r"docs\-(" + "|".join(variants) + r")\-", re.VERBOSE)

    # matches all other occurrences we need to handle
    BRANCH_RE = re.compile(r"/(" + "|".join(variants) + r")", re.VERBOSE)

    new_contents = []
    for line in contents.splitlines():
        if BRANCH_RE.search(line) is not None:
            if "gitlab" in line:  # gitlab links
                replacement = (
                    "/v%s" % version
                    if version is not None
                    else f"/{default_branch}"
                )
                line = BRANCH_RE.sub(replacement, line)
            if ("docs-latest" in line) or ("docs-stable" in line):
                # our doc server
                replacement = (
                    "/v%s" % version
                    if version is not None
                    else f"/{default_branch}"
                )
                line = BRANCH_RE.sub(replacement, line)
        if DOC_IMAGE.search(line) is not None:
            replacement = (
                "docs-v%s-" % version if version is not None else "docs-latest-"
            )
            line = DOC_IMAGE.sub(replacement, line)
        new_contents.append(line)

    return "\n".join(new_contents) + "\n"


def _pin_versions_of_packages_list(
    packages_list: list[str],
    dependencies_versions: list[Requirement],
) -> list[str]:
    """Adds its version to each package according to a dictionary of versions.

    Modifies ``packages_list`` in-place.

    Iterates over ``packages_list`` and sets the version to be the corresponding
    one in ``dependencies_versions``.

    Edge cases:

        **Package not in ``dependencies_versions``**: The package will not be
            pinned.

        **Package already has version specifier**: Raises a ``ValueError``.

    Arguments:

        packages_list: The packages to pin.

        dependencies_versions: All the known packages with their desired version
            pinning.

    Raises:

        ``ValueError`` if a version in ``dependencies_versions`` conflicts with
        an already present pinning in ``packages_list``.
    """

    # Check that there is not the same dependency twice in the pins
    seen = set()
    for d in dependencies_versions:
        if d.key in seen:
            raise NotImplementedError(
                "Pinning with more than one specification per dependency not"
                "supported."
            )
        seen.add(d.key)

    # Make it easier to retrieve the dependency pin for each package.
    dependencies_dict = {d.key: d for d in dependencies_versions}

    results = []

    # package is the dependency we want to pin
    for pkg_id, package in enumerate(packages_list):
        results.append(package)

        # Get the dependency package version specifier if already present.
        pkg_req = Requirement.parse(package)

        if pkg_req.url is not None:
            logger.warning(
                "Ignoring dependency '%s' as it is specified with a url (%s).",
                pkg_req.key,
                pkg_req.url,
            )

        # Retrieve this dependency's constraint Requirement object
        desired_pin = dependencies_dict.get(pkg_req.key)

        if desired_pin is None:
            logger.warning(
                "Dependency '%s' is not available in constraints. Skipping "
                "pinning. Consider adding this package to your dev-profile "
                "constraints file.",
                pkg_req.key,
            )
            continue

        # A Requirement is composed of:
        #   key[extras]@ url ; marker
        # Or
        #   key[extras]specifier; marker
        # Where extras and marker are optional

        # The following handles those different fields

        if desired_pin.url is not None:
            logger.info(
                "Pinning of %s will be done with a URL (%s).",
                pkg_req.key,
                desired_pin.url,
            )
        else:
            # Build the 'specs' field
            if len(desired_pin.specs) == 0:
                logger.warning(
                    "Dependency '%s' has no version specifier in constraints "
                    "'%s'. Skipping pinning.",
                    pkg_req.key,
                    desired_pin,
                )
                continue

            # If version specifiers are already present in that dependency
            if len(pkg_req.specs) > 0:
                raise ValueError(
                    f"You cannot specify a version for the dependency {pkg_req}"
                )
            desired_specs = desired_pin.specs

            # Set the version of that dependency to the pinned one.
            specs_str = ",".join("".join(s) for s in desired_specs)

        # Build the 'marker' field
        if pkg_req.marker is not None:
            raise ValueError(
                f"You can not specify a marker for the dependency {pkg_req}! "
                f"({pkg_req.marker})"
            )
        marker_str = ""
        if desired_pin.marker is not None:
            marker_str = f"; {desired_pin.marker}"

        # Build the 'extras' field
        if len(pkg_req.extras) > 0:
            raise ValueError(
                f"You can not specify extras for the dependency {pkg_req}! "
                f"({pkg_req.extras})"
            )

        extras_str = ""
        if len(desired_pin.extras) > 0:
            extras_str = f"[{','.join(desired_pin.extras)}]"

        # Assemble the dependency specification in one string
        if desired_pin.url is not None:
            final_str = "".join(
                (
                    pkg_req.key,
                    extras_str,
                    "@ ",
                    desired_pin.url,
                    " ",
                    marker_str,
                )
            )
        else:
            final_str = "".join(
                (pkg_req.key, extras_str, specs_str, marker_str)
            )

        # Replace the package specification with the pinned version
        packages_list[pkg_id] = str(Requirement.parse(final_str))
        logger.debug("Package pinned: %s", packages_list[pkg_id])

    return packages_list


def _update_pyproject(
    contents: str,
    version: str,
    default_branch: str,
    update_urls: bool,
    profile: Profile | None = None,
) -> str:
    """Updates contents of pyproject.toml to make it release/latest ready.

    - Sets the project.version field to the given version.
    - Pins the dependencies version to the ones in the given dev-profile.
    - Saves the dev-profile's url and commit in the pyproject.toml.
    - Updates the documentation URLs to point specifically to the given version.

    Arguments:

        contents: Text of the ``pyproject.toml`` file from a package

        version: Format of the version string is '#.#.#'

        default_branch: The name of the default project branch to use

        update_urls: If set to ``True``, then also updates the relevant URL
          links considering the version number provided at ``version``.

        profile: Used to retrieve and note the current dev-profile commit.

    Returns:

        New version of ``pyproject.toml`` with all replaces done
    """

    variants = {
        "available",
        "latest",
        "main",
        "master",
        "stable",
        default_branch,
        packaging.version.VERSION_PATTERN,
    }

    data = tomlkit.loads(contents)

    if (
        re.match(packaging.version.VERSION_PATTERN, version, re.VERBOSE)
        is not None
    ):
        logger.info(
            "Updating pyproject.toml version from '%s' to '%s'",
            data.get("project", {}).get("version", "unknown version"),
            version,
        )
        data["project"]["version"] = version

    else:
        logger.info(
            "Not setting project version on pyproject.toml as it is "
            f"not PEP-440 compliant (given value: `{version}')"
        )

    # Pinning of the dependencies packages version
    if profile is not None:
        dependencies_pins = profile.python_constraints()

        # Main dependencies
        logger.info("Pinning versions of dependencies.")
        pkg_deps = data.get("project", {}).get("dependencies", [])
        _pin_versions_of_packages_list(
            packages_list=pkg_deps,
            dependencies_versions=dependencies_pins,
        ),

        # Optional dependencies
        opt_pkg_deps = data.get("project", {}).get("optional-dependencies", [])
        for pkg_group in opt_pkg_deps:
            logger.info(
                "Pinning versions of optional dependencies group `%s`.",
                pkg_group,
            )
            _pin_versions_of_packages_list(
                packages_list=opt_pkg_deps[pkg_group],
                dependencies_versions=dependencies_pins,
            )

        # Registering dev-profile version
        logger.info("Annotating pyproject with current dev-profile commit.")
        logger.debug("Using dev-profile at '%s'", profile._basedir)
        profile_repo = Repo(profile._basedir)
        if profile_repo.is_dirty():
            raise RuntimeError(
                "dev-profile was modified and is dirty! Unable to ensure a "
                "commit corresponds to the current state of that repository. "
                "Please commit and push your changes."
            )
        logger.debug("Fetching origin of dev-profile.")
        profile_repo.remotes.origin.fetch()
        logger.debug("Checking that the local commits are available on origin.")
        commits_ahead = [
            c for c in profile_repo.iter_commits("origin/main..HEAD")
        ]
        if len(commits_ahead) != 0:
            raise RuntimeError(
                "Local commits of dev-profile were not pushed to origin!\n"
                f"(dev-profile HEAD is {len(commits_ahead)} commits ahead of "
                "origin).\n "
                "Please 'git push' your modifications or revert them.\n"
                "We enforce this so a dev-profile version can always be "
                "retrieved."
            )
        logger.debug("Checking we are up to date with origin.")
        commits_behind = [
            c for c in profile_repo.iter_commits("HEAD..origin/main")
        ]
        if len(commits_behind) != 0:
            logger.warning(
                "Your local dev-profile is not up to date with the origin "
                "remote. It is fine as long as you know what you are doing, "
                "but you should consider 'git pull' the latest changes.\n"
                "(dev-profile HEAD is %d commits behind origin)",
                len(commits_behind),
            )
        # Actually add the dev-profile commit hash to pyproject.toml
        data["profile"] = tomlkit.table()
        data["profile"].add(
            "repository_url",
            tomlkit.item(profile_repo.remotes.origin.url).indent(4),
        )
        data["profile"].add(
            "commit_hash",
            tomlkit.item(profile_repo.commit("HEAD").hexsha).indent(4),
        )

    if not update_urls:
        return tomlkit.dumps(data)

    # matches all other occurrences we need to handle
    BRANCH_RE = re.compile(r"/(" + "|".join(variants) + r")", re.VERBOSE)

    # sets the various URLs
    url = data["project"].get("urls", {}).get("documentation")
    if (url is not None) and (BRANCH_RE.search(url) is not None):
        replacement = (
            "/v%s" % version if version is not None else f"/{default_branch}"
        )
        data["project"]["urls"]["documentation"] = BRANCH_RE.sub(
            replacement, url
        )

    return tomlkit.dumps(data)


def get_latest_tag_name(
    gitpkg: gitlab.v4.objects.projects.Project,
) -> str | None:
    """Find the name of the latest tag for a given package in the format
    '#.#.#'.

    Arguments:

        gitpkg: gitlab package object

    Returns:

        The name of the latest tag in format '#.#.#'. ``None`` if no tags for
        the package were found.
    """

    # get 50 latest tags as a list
    latest_tags = gitpkg.releases.list(all=True)
    if not latest_tags:
        return None
    # create list of tags' names but ignore the first 'v' character in each name
    # also filter out non version tags
    tag_names = [
        tag.name[1:]
        for tag in latest_tags
        if StrictVersion.version_re.match(tag.name[1:])
    ]
    if not tag_names:  # no tags were found.
        return None
    # sort them correctly according to each subversion number
    tag_names.sort(key=StrictVersion)
    # take the last one, as it is the latest tag in the sorted tags
    latest_tag_name = tag_names[-1]
    return latest_tag_name


def get_next_version(
    gitpkg: gitlab.v4.objects.projects.Project, bump: str
) -> str:
    """Returns the next version of this package to be tagged.

    Arguments:

        gitpkg: gitlab package object

        bump: what to bump (can be "major", "minor", or "patch" versions)


    Returns:

        The new version of the package (to be tagged)


    Raises:

        ValueError: if the latest tag retrieve from the package does not
            conform with the subset of PEP440 we use (e.g. "v1.2.3b1").
    """

    # if we bump the version, we need to find the latest released version for
    # this package
    assert bump in ("major", "minor", "patch")

    # find the correct latest tag of this package (without 'v' in front),
    # None if there are no tags yet
    latest_tag_name = get_latest_tag_name(gitpkg)

    if latest_tag_name is None:
        if bump == "major":
            return "v1.0.0"

        elif bump == "minor":
            return "v0.1.0"

        # patch
        return "v0.0.1"

    # check that it has expected format #.#.#
    # latest_tag_name = Version(latest_tag_name)
    m = re.match(r"(\d+\.\d+\.\d+)", latest_tag_name)
    if not m:
        raise ValueError(
            "The latest tag name {} in package {} has "
            "unknown format".format(
                "v" + latest_tag_name,
                gitpkg.attributes["path_with_namespace"],
            )
        )

    # increase the version accordingly
    major, minor, patch = latest_tag_name.split(".")

    if bump == "major":
        return f"v{int(major)+1}.0.0"

    if bump == "minor":
        return f"v{major}.{int(minor)+1}.0"

    # it is a patch release, proceed with caution for pre-releases

    # handles possible pre-release (alpha, beta, etc) extensions
    pre_releases = ("a", "b", "c", "rc", "dev")
    matches_pre_release = next((k for k in pre_releases if k in patch), "")
    if len(matches_pre_release) != 0:
        patch = patch.split(matches_pre_release)[0]
        # in these cases, we just need to respect the current patch number for
        # a patch release - this doesn't matter otherwise
        patch_int = int(patch) - 1
    else:
        patch_int = int(patch)

    # increment the last number in 'v#.#.#'
    return f"v{major}.{minor}.{patch_int+1}"


def update_files_at_default_branch(
    gitpkg: gitlab.v4.objects.projects.Project,
    files_dict: dict[str, str],
    message: str,
    dry_run: bool,
) -> None:
    """Update (via a commit) files of a given gitlab package, directly on the
    default project branch.

    Arguments:

        gitpkg: gitlab package object

        files_dict: Dictionary of file names and their contents (as text)

        message: Commit message

        dry_run: If True, nothing will be committed or pushed to GitLab
    """

    data = {
        "branch": gitpkg.default_branch,
        "commit_message": message,
        "actions": [],
    }  # v4

    # add files to update
    for filename in files_dict.keys():
        update_action = dict(action="update", file_path=filename)
        update_action["content"] = files_dict[filename]
        data["actions"].append(update_action)  # type: ignore

    logger.debug(
        "Committing changes in files (%s) to branch '%s'",
        ", ".join(files_dict.keys()),
        gitpkg.default_branch,
    )
    if not dry_run:
        commit = gitpkg.commits.create(data)
        logger.info(
            "Created commit %s at %s (branch=%s)",
            commit.short_id,
            gitpkg.attributes["path_with_namespace"],
            gitpkg.default_branch,
        )


def _get_last_pipeline(
    gitpkg: gitlab.v4.objects.projects.Project,
) -> gitlab.v4.objects.pipelines.Pipeline:
    """Returns the last pipeline of the project.

    Arguments:

        gitpkg: gitlab package object

    Returns:

        The gitlab object of the pipeline
    """

    # wait for 10 seconds to ensure that if a pipeline was just submitted,
    # we can retrieve it
    time.sleep(10)

    # get the last pipeline
    return gitpkg.pipelines.list(per_page=1, page=1)[0]


def wait_for_pipeline_to_finish(
    gitpkg: gitlab.v4.objects.projects.Project,
    pipeline_id: int | None,
) -> None:
    """Using sleep function, wait for the latest pipeline to finish building.

    This function pauses the script until pipeline completes either
    successfully or with error.

    Arguments:

        gitpkg: gitlab package object
        pipeline_id: id of the pipeline for which we are waiting to finish
        dry_run: If True, outputs log message and exit. There wil be no
                 waiting.
    """

    sleep_step = 30
    max_sleep = 120 * 60  # two hours

    logger.warning(
        f"Waiting for the pipeline {pipeline_id} of "
        f"`{gitpkg.attributes['path_with_namespace']}' to finish",
    )
    logger.warning("Do **NOT** interrupt!")

    if pipeline_id is None:
        return

    # retrieve the pipeline we are waiting for
    pipeline = gitpkg.pipelines.get(pipeline_id)

    # probe and wait for the pipeline to finish
    slept_so_far = 0

    while pipeline.status == "running" or pipeline.status == "pending":
        time.sleep(sleep_step)
        slept_so_far += sleep_step
        if slept_so_far > max_sleep:
            raise ValueError(
                "I cannot wait longer than {} seconds for "
                "pipeline {} to finish running!".format(max_sleep, pipeline_id)
            )
        # probe gitlab to update the status of the pipeline
        pipeline = gitpkg.pipelines.get(pipeline_id)

    # finished running, now check if it succeeded
    if pipeline.status != "success":
        raise ValueError(
            "Pipeline {} of project {} exited with "
            'undesired status "{}". Release is not possible.'.format(
                pipeline_id,
                gitpkg.attributes["path_with_namespace"],
                pipeline.status,
            )
        )

    logger.info(
        "Pipeline %s of package %s SUCCEEDED. Continue processing.",
        pipeline_id,
        gitpkg.attributes["path_with_namespace"],
    )


def _cancel_last_pipeline(gitpkg: gitlab.v4.objects.projects.Project) -> None:
    """Cancel the last started pipeline of a package.

    Arguments:

        gitpkg: gitlab package object
    """
    pipeline = _get_last_pipeline(gitpkg)
    logger.info(
        "Cancelling the last pipeline %s of project %s",
        pipeline.id,
        gitpkg.attributes["path_with_namespace"],
    )
    pipeline.cancel()


def _get_differences(orig: str, changed: str, fname: str) -> str:
    """Calculates the unified diff between two files readout as strings.

    Arguments:

        orig: The original file

        changed: The changed file, after manipulations

        fname: The name of the file


    Returns:

        The unified differences between the changes.
    """
    differences = difflib.unified_diff(
        orig.split("\n"),
        changed.split("\n"),
        fromfile=fname,
        tofile=fname + ".new",
        n=0,
        lineterm="",
    )

    return "\n".join(differences)


def release_package(
    gitpkg: gitlab.v4.objects.projects.Project,
    tag_name: str,
    tag_comments: str,
    dry_run: bool = False,
    profile: Profile | None = None,
) -> int | None:
    """Releases a package.

    The provided tag will be annotated with a given list of comments. Files
    such as ``README.md`` and ``pyproject.toml`` will be updated according to
    the release procedures.


    Arguments:

        gitpkg: gitlab package object

        tag_name: The name of the release tag

        tag_comments_list: New annotations for this tag in a form of list

        dry_run: If ``True``, nothing will be committed or pushed to GitLab

        profile: An instance of :class:`idiap_devtools.profile.Profile` used to
            retrieve the specifiers to pin the package's dependencies in
            ``pyproject.toml``.

    Returns:

        The (integer) pipeline identifier, or None, if a pipeline was not
        actually started (e.g. ``dry_run`` is set to ``True``)
    """

    # 1. Replace branch tag in Readme to new tag, change version file to new
    # version tag. Add and commit to gitlab
    version_number = tag_name[1:]  # remove 'v' in front

    readme_file = gitpkg.files.get(
        file_path="README.md", ref=gitpkg.default_branch
    )

    readme_contents_orig = readme_file.decode().decode()
    readme_contents = _update_readme(
        readme_contents_orig, version_number, gitpkg.default_branch
    )
    if dry_run:
        d = _get_differences(readme_contents_orig, readme_contents, "README.md")
        logger.info(f"Changes to release (from latest):\n{d}")

    pyproject_file = gitpkg.files.get(
        file_path="pyproject.toml", ref=gitpkg.default_branch
    )

    pyproject_contents_orig = pyproject_file.decode().decode()
    pyproject_contents = _update_pyproject(
        contents=pyproject_contents_orig,
        version=version_number,
        default_branch=gitpkg.default_branch,
        update_urls=True,
        profile=profile,
    )
    if dry_run:
        d = _get_differences(
            pyproject_contents_orig, pyproject_contents, "pyproject.toml"
        )
        logger.info(f"Changes to release (from latest):\n{d}")

    # commit and push changes
    update_files_at_default_branch(
        gitpkg,
        {"README.md": readme_contents, "pyproject.toml": pyproject_contents},
        "Increased stable version to %s" % version_number,
        dry_run,
    )

    if not dry_run:
        # cancel running the pipeline triggered by the last commit
        _cancel_last_pipeline(gitpkg)

    # 2. Tag package with new tag and push
    logger.info('Tagging "%s"', tag_name)
    logger.debug("Updating tag comments with:\n%s", tag_comments)
    if not dry_run:
        params = {
            "name": tag_name,
            "tag_name": tag_name,
            "ref": gitpkg.default_branch,
        }
        if tag_comments:
            params["description"] = tag_comments
        gitpkg.releases.create(params)

    # get the pipeline that is actually running with no skips
    running_pipeline = _get_last_pipeline(gitpkg)

    # 3. Re-store the original README, bump the pyproject.toml release by a
    # (beta) notch

    # sets the next beta version
    major, minor, patch = version_number.split(".")
    next_version_number = f"{major}.{minor}.{int(patch) + 1}b0"

    pyproject_contents_latest = _update_pyproject(
        contents=pyproject_contents_orig,
        version=next_version_number,
        default_branch=gitpkg.default_branch,
        update_urls=False,
    )
    # commit and push changes
    update_files_at_default_branch(
        gitpkg,
        {
            "README.md": readme_contents_orig,
            "pyproject.toml": pyproject_contents_latest,
        },
        "Increased latest version to %s [skip ci]" % next_version_number,
        dry_run,
    )
    if dry_run:
        d = _get_differences(
            pyproject_contents, pyproject_contents_latest, "pyproject.toml"
        )
        logger.info(f"Changes from release (to latest):\n{d}")

    return running_pipeline.id
