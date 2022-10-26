FROM python:3.10.8-alpine3.16

RUN pip3 install fresh-deps \
      --no-cache-dir \
      --disable-pip-version-check \
      --root-user-action=ignore

WORKDIR /workdir
