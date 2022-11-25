from d42 import schema

GitLabMergeRequestSchema = schema.dict({
    "source_branch": schema.str.len(1, 32),
    "web_url": schema.str.regex(r"https://gitlab\.com/[a-z]+/merge_requests/[0-9]+")
})
