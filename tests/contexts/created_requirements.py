import os
from hashlib import sha256
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List, Tuple

import vedro
from config import Config


@vedro.context
def created_requirements_in(packages: List[str]) -> str:
    filename, _ = _create_tmp_file("\n".join(packages), ".in")
    return filename


@vedro.context
def created_requirements_txt(packages: List[str], *,
                             index_url: str = Config.PyPi.URL) -> Tuple[str, str]:
    output = "\n".join([f"--index-url {index_url}", *packages])
    return _create_tmp_file(f"{output}\n", ".txt")


def _create_tmp_file(content: str, suffix: str) -> Tuple[str, str]:
    filehash = sha256(content.encode()).hexdigest()
    with NamedTemporaryFile(suffix=suffix, dir=Path("."), delete=False) as f:
        filename = f.name
        f.write(content.encode())

    vedro.defer(os.unlink, filename)

    return filename, filehash
