from pathlib import Path
from typing import List, Optional, Union

from gitlab import Gitlab

from ._service_api import MergeRequest, ServiceAPI

__all__ = ("GitLabAPI",)


class GitLabAPI(ServiceAPI):
    def __init__(self, server_url: str, private_token: str,
                 project_id: str, default_branch: str) -> None:
        self._gitlab = Gitlab(server_url, private_token, api_version="4")
        self._project_id = project_id
        self._default_branch = default_branch
        self._project = self._gitlab.projects.get(self._project_id)

    # Docs https://docs.gitlab.com/ee/api/users.html#list-users
    def get_user_id(self, username: str) -> Union[str, None]:
        users = self._gitlab.users.list(username=username)
        if len(users) == 0:
            return None
        return str(users[0].id)  # type: ignore

    # Docs https://docs.gitlab.com/ee/api/merge_requests.html#list-merge-requests
    def get_merge_requests(self) -> List[MergeRequest]:
        merge_requests = []
        for mr in self._project.mergerequests.list(state="opened", per_page=50, iterator=True):
            merge_requests.append(MergeRequest(mr.source_branch, mr.web_url))
        return merge_requests

    def _get_file_content(self, path: Path) -> str:
        with open(path) as f:
            return f.read()

    # https://docs.gitlab.com/ee/api/commits.html#create-a-commit-with-multiple-files-and-actions
    def commit_file(self, path: Path, message: str, source_branch: str) -> None:
        self._project.commits.create({
            "id": self._project_id,
            "branch": source_branch,
            "commit_message": message,
            "start_branch": self._default_branch,
            "actions": [
                {
                    "action": "update",
                    "file_path": str(path),
                    "content": self._get_file_content(path),
                }
            ]
        })

    # Docs https://docs.gitlab.com/ee/api/merge_requests.html#create-mr
    def create_merge_request(self, source_branch: str, title: str, *,
                             assignee_id: Optional[str] = None) -> MergeRequest:
        merge_request = self._project.mergerequests.create({
            "source_branch": source_branch,
            "target_branch": self._default_branch,
            "title": title,
            "remove_source_branch": True,
            "squash": True,
            "assignee_id": assignee_id,
        })
        return MergeRequest(source_branch, merge_request.web_url)
