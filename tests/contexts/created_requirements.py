import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List

import vedro
from config import Config


@vedro.context
def created_requirements_in(packages: List[str]) -> str:
    return _create_tmp_file("\n".join(packages), ".in")


@vedro.context
def created_requirements_txt(packages: List[str], *, index_url: str = Config.PyPi.URL) -> str:
    output = "\n".join([f"--index-url {index_url}", *packages])
    return _create_tmp_file(f"{output}\n", ".txt")


def _create_tmp_file(content: str, suffix: str) -> str:
    with NamedTemporaryFile(suffix=suffix, dir=Path("."), delete=False) as f:
        filename = f.name
        f.write(content.encode())

    vedro.defer(os.unlink, filename)

    return filename
