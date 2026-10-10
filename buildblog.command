#!/bin/bash

# Move into the GitHub repository
cd "$(dirname "$0")"

# Activate the virtual environment one directory above the repo
source ../.venv/bin/activate

# Build all blog posts
python3 build_blog.py

if python3 build_blog.py; then
    echo ""
    echo "✓ Blog build complete."
else
    echo ""
    echo "✗ Blog build FAILED."
fi

echo ""
read -p "Press Enter to close..."