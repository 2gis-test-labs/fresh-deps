import asyncio
from typing import Tuple

import vedro
from config import Config


class FreshDepsCLI(vedro.Interface):
    def __init__(self, gitlab_url: str = Config.GitLab.URL,
                 pypi_index_url: str = Config.PyPi.URL) -> None:
        self.gitlab_url = gitlab_url
        self.pypi_index_url = pypi_index_url

    async def run(self, requirements_in: str, requirements_out: str, *,
                  gitlab_project_id: int, gitlab_private_token: str) -> Tuple[str, str]:
        cmd = f'''
            fresh-deps {requirements_in} \
                --output-file={requirements_out} \
                --pypi-index-url={self.pypi_index_url} \
                --gitlab-project-id={gitlab_project_id} \
                --gitlab-private-token={gitlab_private_token} \
                --gitlab-url={self.gitlab_url}
        '''.strip()
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return stdout.decode(), stderr.decode()
