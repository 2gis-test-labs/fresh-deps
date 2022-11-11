from typing import Dict

import jj
import vedro
from jj.mock import Mocked, mocked


@vedro.context
def mocked_gitlab_mr(project: Dict[str, str], web_url: str) -> Mocked:
    matcher = jj.match("POST", "/api/v4/projects/{project_id}/merge_requests")
    response = jj.Response(json={"web_url": web_url})
    return mocked(matcher, response)
