from typing import Dict

import jj
import vedro
from jj.mock import Mocked, mocked


@vedro.context
def mocked_gitlab_commits(project: Dict[str, str]) -> Mocked:
    matcher = jj.match("POST", "/api/v4/projects/{project_id}/repository/commits")
    response = jj.Response(json={})
    return mocked(matcher, response)
