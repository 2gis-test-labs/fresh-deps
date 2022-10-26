import argparse
from os import environ
from pathlib import Path
from typing import Any, Callable

from ._dependency_updater import DependencyUpdater, MergeRequestExists, NothingToUpdate
from ._gitlab_api import GitLabAPI

__all__ = ("update_dependencies",)


def update_dependencies(logger: Callable[[str], Any] = print) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("requirements_in", type=Path)
    parser.add_argument("requirements_out", type=Path, nargs="?", default=None)

    parser.add_argument("--gitlab-url",
                        default=environ.get("CI_SERVER_URL", "https://gitlab.com"))
    parser.add_argument("--gitlab-project-id",
                        default=environ.get("CI_PROJECT_ID", ""))
    parser.add_argument("--gitlab-default-branch",
                        default=environ.get("CI_DEFAULT_BRANCH", "main"))
    parser.add_argument("--gitlab-private-token",
                        default=environ.get("CI_PRIVATE_TOKEN", ""))

    args = parser.parse_args()

    requirements_in = args.requirements_in.absolute().relative_to(Path.cwd())
    assert requirements_in.exists(), f"File '{requirements_in}' does not exist"

    if args.requirements_out is None:
        requirements_out = requirements_in.with_suffix(".txt")
    else:
        requirements_out = args.requirements_out.absolute().relative_to(Path.cwd())
    assert requirements_out.exists(), f"File '{requirements_out}' does not exist"

    assert args.gitlab_project_id, "Project ID is required"
    assert args.gitlab_private_token, "Private token is required"

    try:
        service_api = GitLabAPI(args.gitlab_url, args.gitlab_private_token,
                                args.gitlab_project_id, args.gitlab_default_branch)
    except BaseException as e:
        raise ConnectionError(f"Could not connect to GitLab: '{args.gitlab_url}'") from e

    dependency_updater = DependencyUpdater(service_api)
    try:
        merge_request = dependency_updater.update(requirements_in, requirements_out)
    except NothingToUpdate as e:
        logger(f"Nothing to update ({e})")
    except MergeRequestExists as e:
        logger(f"Merge request already exists ({e})")
    else:
        logger(f"New merge request created: {merge_request.url}")
