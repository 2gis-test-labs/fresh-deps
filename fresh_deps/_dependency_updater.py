from hashlib import sha256
from pathlib import Path
from time import time
from typing import Optional

from plumbum import local

from ._service_api import MergeRequest, ServiceAPI

__all__ = ("DependencyUpdater", "NothingToUpdate", "MergeRequestExists",
           "AnotherMergeRequestExists", "UserNotFound",)


class _DependencyUpdaterException(Exception):
    pass


class NothingToUpdate(_DependencyUpdaterException):
    pass


class MergeRequestExists(_DependencyUpdaterException):
    pass


class AnotherMergeRequestExists(_DependencyUpdaterException):
    pass


class UserNotFound(_DependencyUpdaterException):
    pass


class DependencyUpdater:
    def __init__(self, service_api: ServiceAPI, pypi_index_url: str) -> None:
        self._service_api = service_api
        self._py_index_url = pypi_index_url

    def _get_file_hash(self, path: Path) -> str:
        with open(path, "r") as f:
            content = f.readlines()
        lines = [x for x in content if x.strip() and not x.strip().startswith("#")]
        return sha256("".join(lines).encode()).hexdigest()

    def _run_pip_compile(self, requirements_in: Path, requirements_out: Path) -> None:
        local["pip-compile"](requirements_in, "--upgrade",
                             "--index-url", self._py_index_url,
                             "--output-file", requirements_out)

    def update(self, requirements_in: Path, requirements_out: Path, *,
               assignee: Optional[str] = None,
               allow_multiple_mrs: bool = False,
               branch_prefix: str = "fresh-deps") -> MergeRequest:
        commit_message = "update dependencies"
        merge_request_title = "fresh-deps: update dependencies"

        assignee_id = None
        if assignee is not None:
            assignee_id = self._service_api.get_user_id(assignee)
            if assignee_id is None:
                raise UserNotFound(assignee)

        hash_before = self._get_file_hash(requirements_out)
        self._run_pip_compile(requirements_in, requirements_out)

        hash_after = self._get_file_hash(requirements_out)
        hash_short = hash_after[:10]
        if hash_after == hash_before:
            raise NothingToUpdate(hash_short)

        branch_name = "{}-{}-{}".format(branch_prefix, int(time()), hash_short)
        merge_requests = self._service_api.get_merge_requests()

        for merge_request in merge_requests:
            source_branch = merge_request.source_branch
            if source_branch.startswith(branch_prefix) and source_branch.endswith(hash_short):
                raise MergeRequestExists(merge_request.url)

        for merge_request in merge_requests:
            if merge_request.source_branch.startswith(branch_prefix) and (not allow_multiple_mrs):
                raise AnotherMergeRequestExists(merge_request.url)

        self._service_api.commit_file(requirements_out, commit_message, branch_name)
        mr = self._service_api.create_merge_request(branch_name, merge_request_title,
                                                    assignee_id=assignee_id)
        return mr
