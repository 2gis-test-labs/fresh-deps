import vedro
from config import Config
from plumbum import ProcessExecutionError, local


class FreshDepsCLI(vedro.Interface):
    def __init__(self, gitlab_url: str = Config.GitLab.URL,
                 pypi_index_url: str = Config.PyPi.URL) -> None:
        self.gitlab_url = gitlab_url
        self.pypi_index_url = pypi_index_url

    async def run(self, requirements_in: str, requirements_out: str, *,
                  gitlab_project_id: int, gitlab_private_token: str) -> str:
        try:
            output = local["fresh-deps"](
                requirements_in,
                f"--output-file={requirements_out}",
                f"--pypi-index-url={self.pypi_index_url}",
                f"--gitlab-project-id={gitlab_project_id}",
                f"--gitlab-private-token={gitlab_private_token}",
                f"--gitlab-url={self.gitlab_url}"
            )
        except ProcessExecutionError as e:
            output = repr(e)
        return output
