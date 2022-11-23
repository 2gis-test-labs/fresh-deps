from d42 import schema

GitLabMergeRequestSchema = schema.dict({
    "source_branch": schema.str.len(1, 32),
    "web_url": schema.str.len(1, 32),
})
