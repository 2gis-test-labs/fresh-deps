def make_branch_name(hash: str) -> str:
    hash_short = hash[:10]
    return f"fresh-deps-{hash_short}"
