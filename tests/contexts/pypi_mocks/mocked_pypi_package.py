import io
import tarfile
from contextlib import asynccontextmanager
from hashlib import sha256
from typing import Any, Dict, Generator, List, Tuple

import jj
import vedro
from jj.mock import _REMOTE_MOCK_URL, Mocked, mocked


def _create_tar(package: str, version: str) -> bytes:
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w:gz") as tar:
        info = tarfile.TarInfo(f"{package}-{version}.tar.gz/setup.py")

        data = f"from setuptools import setup\nsetup(name='{package}', version='{version}')\n"
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data.encode()))

    return output.getvalue()


def _make_version_info(package: str, version: str) -> Tuple[Dict[str, Any], bytes]:
    tar = _create_tar(package, version)
    version_info = {
        "filename": f"{package}-{version}.tar.gz",
        "hashes": {
            "sha256": sha256(tar).hexdigest()
        },
        "requires-python": None,
        "url": f"{_REMOTE_MOCK_URL}/packages/{package}-{version}.tar.gz",
        "yanked": False,
    }
    return version_info, tar


@vedro.context
@asynccontextmanager
async def mocked_pypi_package(package: str,
                              versions: List[str]) -> Generator[Tuple[Mocked, Mocked], None, None]:
    assert len(versions) > 0
    latest_version = versions[0]

    version_info, tar = _make_version_info(package, latest_version)
    payload = {
        "meta": {
            "_last-serial": 1,
            "api-version": "1.0"
        },
        "name": package,
        "files": [version_info],
    }
    package_matcher = jj.match("GET", f"/simple/{package}/")
    package_response = jj.Response(json=payload, headers={
        "Content-Type": "application/vnd.pypi.simple.v1+json"
    })
    async with mocked(package_matcher, package_response) as package_mock:
        file_matcher = jj.match("GET", f"/packages/{package}-{latest_version}.tar.gz")
        file_response = jj.Response(body=tar)
        async with mocked(file_matcher, file_response) as file_mock:
            yield package_mock, file_mock
