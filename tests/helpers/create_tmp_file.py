import os
from hashlib import sha256
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Tuple

import vedro


def create_tmp_file(content: str, suffix: str) -> Tuple[str, str]:
    filehash = sha256(content.encode()).hexdigest()
    with NamedTemporaryFile(suffix=suffix, dir=Path("."), delete=False) as f:
        filename = f.name
        f.write(content.encode())

    vedro.defer(os.unlink, filename)

    return filename, filehash
