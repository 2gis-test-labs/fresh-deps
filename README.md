# fresh-deps

[![PyPI](https://img.shields.io/pypi/v/fresh-deps.svg?style=flat-square)](https://pypi.python.org/pypi/fresh-deps/)
[![Python Version](https://img.shields.io/pypi/pyversions/fresh-deps.svg?style=flat-square)](https://pypi.python.org/pypi/fresh-deps/)

## Installation

```shell
$ pip3 install fresh-deps
```

## Usage

```shell
$ fresh-deps requirements.in --gitlab-project-id=<id> --gitlab-private-token=<token>
```

**or via docker**

```shell
$ docker run -v `pwd`:/workdir 2gistestlabs/fresh-deps fresh-deps requirements.in \
    --gitlab-project-id=<id> \
    --gitlab-private-token=<token>
```

### GitLab CI

Add [job](https://docs.gitlab.com/ee/ci/jobs/) and create [scheduled pipeline](https://docs.gitlab.com/ee/ci/pipelines/schedules.html)

```yml
stages:
  - update_dependencies

fresh_deps:
  stage: update_dependencies
  image: 2gistestlabs/fresh-deps:0.4.0
  variables:
    CI_PRIVATE_TOKEN: $GITLAB_PRIVATE_TOKEN
  script:
    - fresh-deps requirements.in
  only:
    - schedules
```

## Docs

```
usage: fresh-deps [-h] [--output-file [OUTPUT_FILE]]
                  [--pypi-index-url PYPI_INDEX_URL]
                  [--gitlab-url GITLAB_URL]
                  [--gitlab-project-id GITLAB_PROJECT_ID]
                  [--gitlab-default-branch GITLAB_DEFAULT_BRANCH]
                  [--gitlab-private-token GITLAB_PRIVATE_TOKEN]
                  [--gitlab-assignee GITLAB_ASSIGNEE]
                  [--gitlab-allow-multiple-mrs]
                  requirements_in

positional arguments:
  requirements_in       Path to requirements.in

options:
  -h, --help            show this help message and exit
  --output-file [OUTPUT_FILE]
                        Path to requirements.txt
  --pypi-index-url PYPI_INDEX_URL
                        PyPI index URL (default: {default_pypi_index})
  --gitlab-url GITLAB_URL
                        GitLab server URL (default: $CI_SERVER_URL or 'https://gitlab.com')
  --gitlab-project-id GITLAB_PROJECT_ID
                        GitLab project ID (defaulT: $CI_PROJECT_ID)
  --gitlab-default-branch GITLAB_DEFAULT_BRANCH
                        GitLab default branch (default: $CI_DEFAULT_BRANCH or 'main')
  --gitlab-private-token GITLAB_PRIVATE_TOKEN
                        GitLab private token (default: $CI_PRIVATE_TOKEN), documentation
                        https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html
  --gitlab-assignee GITLAB_ASSIGNEE
                        GitLab assignee username (example: 'root')
  --gitlab-allow-multiple-mrs
                        Allow multiple opened merge requests
```
