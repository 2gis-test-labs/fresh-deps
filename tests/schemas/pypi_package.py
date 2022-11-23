import string

from d42 import schema

PyPiPackageSchema = schema.dict({
    "name": schema.str.alphabet(string.ascii_lowercase).len(1, 16)
})
