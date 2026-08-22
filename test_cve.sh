#!/bin/bash
python3 -c "
import starlette
v = starlette.__version__.split('.')
major, minor = int(v[0]), int(v[1])
if major == 0 and minor < 49:
    print(f'Vulnerable starlette version: {starlette.__version__}')
    exit(1)
print('Safe starlette version')
"
