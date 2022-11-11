from d42 import schema

GitLabProjectSchema = schema.dict({
    "id": schema.int.min(1).max(2 ** 31 - 1),
    "name": schema.str.len(3, 12),
})
