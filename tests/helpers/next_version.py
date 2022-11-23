import random


def next_version(version: str) -> str:
    parts = [int(x) for x in version.split(".")]

    index = random.choice(range(0, 3))
    parts[index] += 1

    major, minor, patch = parts
    return f"{major}.{minor}.{patch}"
