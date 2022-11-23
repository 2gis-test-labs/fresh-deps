from d42 import fake, schema

VersionPartSchema = schema.int.min(1).max(99)
VersionSchema = schema.list(VersionPartSchema).len(3)


def gen_version() -> str:
    major, minor, patch = fake(VersionSchema)
    return f"{major}.{minor}.{patch}"
