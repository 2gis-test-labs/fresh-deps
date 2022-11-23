from contextlib import AsyncExitStack, asynccontextmanager
from typing import Any, Dict, List

import vedro

from .mocked_gitlab_commits import mocked_gitlab_created_commit
from .mocked_gitlab_mr import mocked_gitlab_created_mr
from .mocked_gitlab_mrs import mocked_gitlab_mrs
from .mocked_gitlab_project import mocked_gitlab_project


@vedro.context
@asynccontextmanager
async def mocked_gitlab(project: Dict[str, str],
                        merge_requests: List[Dict[str, str]], web_url: str) -> Any:
    async with AsyncExitStack() as stack:
        yield {
            "project": await stack.enter_async_context(mocked_gitlab_project(project)),
            "mrs": await stack.enter_async_context(mocked_gitlab_mrs(project, merge_requests)),
            "commit": await stack.enter_async_context(mocked_gitlab_created_commit(project)),
            "mr": await stack.enter_async_context(mocked_gitlab_created_mr(project, web_url)),
        }
