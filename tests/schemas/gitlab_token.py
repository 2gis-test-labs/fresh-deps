from d42 import schema

GitLabPrivateToken = schema.str.regex(r"[a-z]{6,12}")
