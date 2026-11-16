#!/bin/bash

cd "$(dirname "$0")"

../.venv/bin/python3 build_site.py

echo
echo "Build complete."
read -n 1 -s -r -p "Press any key to close..."