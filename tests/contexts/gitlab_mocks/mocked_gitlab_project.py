from typing import Dict

import jj
import vedro
from jj.mock import Mocked, mocked


@vedro.context
def mocked_gitlab_project(project: Dict[str, str]) -> Mocked:
    matcher = jj.match("GET", "/api/v4/projects/{project_id}")
    response = jj.Response(json=project)
    return mocked(matcher, response)
