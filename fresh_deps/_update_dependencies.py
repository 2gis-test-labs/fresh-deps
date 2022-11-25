import argparse
from os import environ
from pathlib import Path
from typing import Any, Callable

from ._dependency_updater import (
    AnotherMergeRequestExists,
    DependencyUpdater,
    MergeRequestExists,
    NothingToUpdate,
)
from ._gitlab_api import GitLabAPI

__all__ = ("update_dependencies",)


def update_dependencies(logger: Callable[[str], Any] = print) -> None:
    parser = argparse.ArgumentParser("fresh-deps",
                                     description="Keep your Python dependencies fresh")

    parser.add_argument("requirements_in", type=Path,
                        help="Path to requirements.in")
    parser.add_argument("--output-file", type=Path, nargs="?", default=None,
                        help="Path to requirements.txt")

    default_pypi_index = "https://pypi.org/simple"
    parser.add_argument("--pypi-index-url", default=default_pypi_index,
                        help="PyPI index URL (default: {default_pypi_index})")

    default_gitlab_url = "https://gitlab.com"
    parser.add_argument("--gitlab-url",
                        default=environ.get("CI_SERVER_URL", default_gitlab_url),
                        help="GitLab server URL "
                             f"(default: $CI_SERVER_URL or '{default_gitlab_url}')")
    parser.add_argument("--gitlab-project-id",
                        default=environ.get("CI_PROJECT_ID", ""),
                        help="GitLab project ID (defaulT: $CI_PROJECT_ID)")
    default_gitlab_branch = "main"
    parser.add_argument("--gitlab-default-branch",
                        default=environ.get("CI_DEFAULT_BRANCH", default_gitlab_branch),
                        help="GitLab default branch "
                             f"(default: $CI_DEFAULT_BRANCH or '{default_gitlab_branch}')")
    docs_url = "https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html"
    parser.add_argument("--gitlab-private-token",
                        default=environ.get("CI_PRIVATE_TOKEN", ""),
                        help="GitLab private token "
                             f"(default: $CI_PRIVATE_TOKEN), documentation {docs_url}")
    parser.add_argument("--gitlab-assignee", help="GitLab assignee username (example: 'root')")
    parser.add_argument("--gitlab-allow-multiple-mrs", action="store_true", default=False,
                        help="Allow multiple opened merge requests")

    args = parser.parse_args()

    requirements_in = args.requirements_in.absolute().relative_to(Path.cwd())
    assert requirements_in.exists(), f"File '{requirements_in}' does not exist"

    if args.output_file is None:
        requirements_out = requirements_in.with_suffix(".txt")
    else:
        requirements_out = args.output_file.absolute().relative_to(Path.cwd())
    assert requirements_out.exists(), f"File '{requirements_out}' does not exist"

    assert args.gitlab_project_id, "Project ID is required"
    assert args.gitlab_private_token, "Private token is required"

    try:
        service_api = GitLabAPI(args.gitlab_url, args.gitlab_private_token,
                                args.gitlab_project_id, args.gitlab_default_branch)
    except BaseException as e:
        raise ConnectionError(f"Could not connect to GitLab: '{args.gitlab_url}'") from e

    dependency_updater = DependencyUpdater(service_api, args.pypi_index_url)
    try:
        merge_request = dependency_updater.update(requirements_in, requirements_out,
                                                  assignee=args.gitlab_assignee or None,
                                                  allow_multiple_mrs=args.gitlab_allow_multiple_mrs)
    except NothingToUpdate as e:
        logger(f"Nothing to update ({e})")
    except MergeRequestExists as e:
        logger(f"Merge request already exists ({e})")
    except AnotherMergeRequestExists as e:
        logger(f"Another merge request exists ({e})")
    else:
        logger(f"New merge request created: {merge_request.url}")
