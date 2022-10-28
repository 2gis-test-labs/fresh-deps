from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Union

__all__ = ("ServiceAPI", "MergeRequest",)


@dataclass
class MergeRequest:
    source_branch: str
    url: str


class ServiceAPI(ABC):
    @abstractmethod
    def get_user_id(self, username: str) -> Union[str, None]:
        pass

    @abstractmethod
    def get_merge_requests(self) -> List[MergeRequest]:
        pass

    @abstractmethod
    def commit_file(self, path: Path, message: str, source_branch: str) -> None:
        pass

    @abstractmethod
    def create_merge_request(self, source_branch: str, title: str, *,
                             assignee_id: Optional[str] = None) -> MergeRequest:
        pass
