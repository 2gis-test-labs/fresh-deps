from typing import Dict, List

import jj
import vedro
from jj.mock import Mocked, mocked


@vedro.context
def mocked_gitlab_mrs(project: Dict[str, str], merge_requests: List[Dict[str, str]]) -> Mocked:
    matcher = jj.match("GET", "/api/v4/projects/{project_id}/merge_requests")
    response = jj.Response(json=merge_requests)
    return mocked(matcher, response)
