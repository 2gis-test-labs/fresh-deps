def next_version(version: str) -> str:
    major, minor, patch = [int(x) for x in version.split(".")]
    return f"{major}.{minor}.{patch + 1}"
