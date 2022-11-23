from typing import List, Tuple

import vedro
from config import Config
from helpers import create_tmp_file


@vedro.context
def created_requirements_in(packages: List[str]) -> str:
    filename, _ = create_tmp_file("\n".join(packages), ".in")
    return filename


@vedro.context
def created_requirements_txt(packages: List[str], *,
                             index_url: str = Config.PyPi.URL) -> Tuple[str, str]:
    output = "\n".join([f"--index-url {index_url}", *packages])
    return create_tmp_file(f"{output}\n", ".txt")
