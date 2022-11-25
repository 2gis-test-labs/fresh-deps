import vedro
from contexts import (
    created_requirements_in,
    created_requirements_txt,
    mocked_gitlab_mrs,
    mocked_gitlab_project,
    mocked_pypi_package,
)
from d42 import fake
from district42 import schema
from helpers import gen_version, make_branch_name, next_version
from interfaces import FreshDepsCLI
from jj_district42 import HistorySchema
from schemas import (
    GitLabMergeRequestSchema,
    GitLabPrivateToken,
    GitLabProjectSchema,
    PyPiPackageSchema,
)


class Scenario(vedro.Scenario):
    subject = "try to upgrade requirements (opened mr exists)"

    def given_package(self):
        self.package_name = fake(PyPiPackageSchema["name"])

    def given_requirements_in(self):
        self.req_in = created_requirements_in([self.package_name])

    def given_requirements_txt(self):
        self.fixed_version = gen_version()
        self.req_txt, self.hash_before = created_requirements_txt([
            f"{self.package_name}=={self.fixed_version}"
        ])

    def given_requirements_hash(self):
        self.next_version = next_version(self.fixed_version)
        _, self.hash_next = created_requirements_txt([
            f"{self.package_name}=={self.next_version}"
        ])

    def given_gitlab_project(self):
        self.project = fake(GitLabProjectSchema)
        self.token = fake(GitLabPrivateToken)

    def given_gitlab_mrs(self):
        self.merge_requests = fake(schema.list([
            GitLabMergeRequestSchema % {
                "source_branch": make_branch_name(self.hash_next)
            },
            GitLabMergeRequestSchema,
        ]))

    def given_latest_version(self):
        self.latest_version = next_version(self.next_version)

    async def when_user_upgrades_requirements(self):
        async with mocked_gitlab_project(self.project) as self.mock_project, \
                   mocked_pypi_package(self.package_name, [self.latest_version]) as self.mock_pypi, \
                   mocked_gitlab_mrs(self.project, self.merge_requests) as self.mock_mrs:
            self.stdout, self.stderr = await FreshDepsCLI().run(
                requirements_in=self.req_in,
                requirements_out=self.req_txt,
                gitlab_project_id=self.project["id"],
                gitlab_private_token=self.token
            )

    def then_it_should_return_info_message(self):
        web_url = self.merge_requests[0]["web_url"]
        assert self.stdout == schema.str(f"Another merge request exists ({web_url})\n")

    def and_it_should_send_request_to_gitlab_projects(self):
        self.gitlab_headers = [..., ["PRIVATE-TOKEN", self.token], ...]
        assert self.mock_project.history == HistorySchema % [{
            "request": {
                "headers":  self.gitlab_headers
            }
        }]

    def and_it_should_send_requests_to_pypi(self):
        package_info_mock, package_file_mock = self.mock_pypi
        assert package_info_mock.history == HistorySchema.len(1)
        assert package_file_mock.history == HistorySchema.len(1)

    def and_it_should_send_request_to_gitlab_mrs(self):
        assert self.mock_mrs.history == HistorySchema % [{
            "request": {
                "params": [
                    ["state", "opened"],
                    ["per_page", "50"],
                ],
                "headers": self.gitlab_headers
            }
        }]
