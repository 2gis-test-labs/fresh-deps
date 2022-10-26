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
