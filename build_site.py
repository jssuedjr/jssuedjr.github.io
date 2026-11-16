#!/usr/bin/env python3
from build_blog import build_blog
from build_projects import build_projects


def main():
    build_blog()
    build_projects()
    print("✓ Entire site rebuilt successfully.")


if __name__ == "__main__":
    main()
