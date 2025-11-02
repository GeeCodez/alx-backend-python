#!/usr/bin/python3
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_pagination

try:
    # Fetch users lazily, 100 at a time
    for page in lazy_paginator(100):
        for user in page:
            print(dict(user))
except BrokenPipeError:
    # This prevents "Broken pipe" error when piping output with | head
    sys.stderr.close()
