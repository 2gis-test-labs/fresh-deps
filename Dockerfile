FROM python:3.10.8-alpine3.16

RUN apk add --no-cache build-base git curl
RUN pip3 install fresh-deps==1.0.0 \
      --no-cache-dir \
      --disable-pip-version-check \
      --root-user-action=ignore

WORKDIR /workdir
