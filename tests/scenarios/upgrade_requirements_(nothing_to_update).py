import vedro
from contexts import (
    created_requirements_in,
    created_requirements_txt,
    mocked_gitlab_project,
    mocked_pypi_package,
)
from d42 import fake
from district42 import schema
from interfaces import FreshDepsCLI
from schemas import GitLabPrivateToken, GitLabProjectSchema, PyPiPackageSchema


class Scenario(vedro.Scenario):
    subject = "upgrade requirements (nothing to update)"

    def given_package(self):
        self.package_name = fake(PyPiPackageSchema)["name"]
        self.package_version = "0.1.1"

    def given_requirements(self):
        req = f"{self.package_name}=={self.package_version}"
        self.req_in = created_requirements_in([req])
        self.req_out = created_requirements_txt([req])

    def given_gitlab_project(self):
        self.project = fake(GitLabProjectSchema)
        self.token = fake(GitLabPrivateToken)

    async def when_user_upgrades_requirements(self):
        async with mocked_gitlab_project(self.project), \
                   mocked_pypi_package(self.package_name, [self.package_version]):
            self.output = await FreshDepsCLI().run(self.req_in, self.req_out,
                                                   gitlab_project_id=self.project["id"],
                                                   gitlab_private_token=self.token)

    def then_it_should_return_success_message(self):
        assert self.output == schema.str.contains("Nothing to update")
