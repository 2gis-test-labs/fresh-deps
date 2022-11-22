import vedro
from contexts import (
    created_requirements_in,
    created_requirements_txt,
    mocked_gitlab_project,
    mocked_pypi_package,
)
from d42 import fake
from district42 import schema
from helpers import gen_version
from interfaces import FreshDepsCLI
from jj_district42 import HistorySchema
from schemas import GitLabPrivateToken, GitLabProjectSchema, PyPiPackageSchema


class Scenario(vedro.Scenario):
    subject = "try to upgrade requirements (nothing to update)"

    def given_package(self):
        self.package_name = fake(PyPiPackageSchema["name"])

    def given_requirements_in(self):
        self.req_in = created_requirements_in([self.package_name])

    def given_requirements_txt(self):
        self.fixed_version = gen_version()
        self.req_out, self.hash = created_requirements_txt([
            f"{self.package_name}=={self.fixed_version}"
        ])

    def given_gitlab_project(self):
        self.project = fake(GitLabProjectSchema)
        self.token = fake(GitLabPrivateToken)

    async def when_user_upgrades_requirements(self):
        async with mocked_gitlab_project(self.project) as self.mock_gitlab, \
                   mocked_pypi_package(self.package_name, [self.fixed_version]) as self.mock_pypi:
            self.output = await FreshDepsCLI().run(self.req_in, self.req_out,
                                                   gitlab_project_id=self.project["id"],
                                                   gitlab_private_token=self.token)

    def then_it_should_return_info_message(self):
        hash_short = self.hash[:10]
        assert self.output == schema.str(f"Nothing to update ({hash_short})\n")

    def and_it_should_send_request_to_gitlab(self):
        assert self.mock_gitlab.history == HistorySchema % [{
            "request": {
                "headers":  [
                    ...,
                    ["PRIVATE-TOKEN", self.token],
                    ...
                ]
            }
        }]

    def and_it_should_send_requests_to_pypi(self):
        package_info_mock, package_file_mock = self.mock_pypi
        assert package_info_mock.history == HistorySchema.len(1)
        assert package_file_mock.history == HistorySchema.len(1)
