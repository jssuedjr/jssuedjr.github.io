from pathlib import Path
from datetime import date, datetime
import html

import frontmatter
import markdown


# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).parent
BLOG_DIRECTORY = ROOT / "blog"
BLOG_INDEX = ROOT / "blog.html"


# ============================================================
# Helpers
# ============================================================

def format_date(value):
    """
    Convert a date from the Markdown front matter into a
    human-readable format.

    Example:
        2026-10-20 -> October 20, 2026
    """

    if isinstance(value, (date, datetime)):
        return value.strftime("%B %d, %Y")

    try:
        parsed_date = datetime.strptime(
            str(value),
            "%Y-%m-%d"
        )

        return parsed_date.strftime("%B %d, %Y")

    except ValueError:
        return str(value)


def load_post(post_directory):
    """
    Read a blog post and return its metadata and Markdown content.
    """

    markdown_file = post_directory / "post.md"

    post = frontmatter.load(markdown_file)

    return post


# ============================================================
# Build individual blog post
# ============================================================

def build_post(post_directory):
    """
    Build:

        blog/<post>/post.md

    into:

        blog/<post>/index.html
    """

    post = load_post(post_directory)

    # --------------------------------------------------------
    # Metadata
    # --------------------------------------------------------

    title = post.get("title", "Untitled Post")
    authors = post.get("authors", "")
    post_date = format_date(post.get("date", ""))
    summary = post.get("summary", "")
    paper_title = post.get("paper_title", "")
    pdf = post.get("pdf", "")

    # --------------------------------------------------------
    # Convert Markdown -> HTML
    # --------------------------------------------------------

    article_html = markdown.markdown(
        post.content,
        extensions=[
            "extra",
            "toc",
            "sane_lists",
        ],
    )

    # --------------------------------------------------------
    # Optional paper information
    # --------------------------------------------------------

    paper_info = ""

    if paper_title or authors or pdf:

        paper_info = """
        <section class="paper-info">
            <h2>Paper Information</h2>
        """

        if paper_title:
            paper_info += f"""
            <p>
                <strong>Paper:</strong>
                {html.escape(str(paper_title))}
            </p>
            """

        if authors:
            paper_info += f"""
            <p>
                <strong>Authors:</strong>
                {html.escape(str(authors))}
            </p>
            """

        if pdf:
            paper_info += f"""
            <p>
                <a
                    class="paper-link"
                    href="{html.escape(str(pdf), quote=True)}"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    View original paper (PDF)
                </a>
            </p>
            """

        paper_info += """
        </section>
        """

    # --------------------------------------------------------
    # Generate page
    # --------------------------------------------------------

    page = f"""<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>{html.escape(str(title))} | Jaime Sued</title>

    <link rel="stylesheet" href="../../styles.css">
    <link rel="stylesheet" href="../../blog.css">


    <!-- MathJax configuration -->

    <script>
        MathJax = {{
            tex: {{
                inlineMath: {{'[+]': [['$', '$']]}}
            }}
        }};
    </script>


    <!-- MathJax -->

    <script
        defer
        src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js">
    </script>

</head>


<body>

    <main class="blog-post">


        <!-- ==========================
             Article Header
             ========================== -->

        <header class="post-header">

            <h1>{html.escape(str(title))}</h1>

            {
                f'<p class="paper-authors">{html.escape(str(authors))}</p>'
                if authors
                else ""
            }

            {
                f'<p class="post-date">{html.escape(str(post_date))}</p>'
                if post_date
                else ""
            }

            {
                f'<p class="post-summary">{html.escape(str(summary))}</p>'
                if summary
                else ""
            }

        </header>


        {paper_info}


        <!-- ==========================
             Article
             ========================== -->

        <article class="post-content">

            {article_html}

        </article>


        <!-- ==========================
             Navigation
             ========================== -->

        <nav class="post-navigation">

            <a href="../../blog.html">
                ← Back to Blog
            </a>

        </nav>


    </main>

</body>

</html>
"""

    output_file = post_directory / "index.html"

    output_file.write_text(
        page,
        encoding="utf-8"
    )

    print(f"✓ Built post: {post_directory.name}")


# ============================================================
# Generate cards for blog.html
# ============================================================

def create_blog_card(post_directory):
    """
    Create the HTML card displayed on the main blog page.
    """

    post = load_post(post_directory)

    title = post.get("title", "Untitled Post")
    summary = post.get("summary", "")
    post_date = format_date(post.get("date", ""))

    folder_name = post_directory.name

    return f"""
        <article class="blog-card">

            <h2>
                <a href="blog/{html.escape(folder_name, quote=True)}/">
                    {html.escape(str(title))}
                </a>
            </h2>

            <p class="blog-card-summary">
                {html.escape(str(summary))}
            </p>

            <p class="blog-card-date">
                {html.escape(str(post_date))}
            </p>

        </article>
    """


# ============================================================
# Build main blog page
# ============================================================

def build_blog_index(post_directories):
    """
    Generate the blog card grid in blog.html.
    """

    cards = "\n".join(
        create_blog_card(directory)
        for directory in post_directories
    )

    page = f"""<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Math Blog | Jaime Sued</title>

    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="blog.css">

</head>


<body>

    <main class="blog-content">


        <!-- ==========================
             Blog Introduction
             ========================== -->

        <header class="blog-header">

            <h1>Mathematical Notes</h1>

            <p>
                A collection of my notes, explanations, and thoughts
                on papers in mathematics, statistics, machine learning,
                probability, and related topics.
            </p>

        </header>


        <!-- ==========================
             Blog Grid
             ========================== -->

        <section class="blog-grid">

            {cards}

        </section>


        <!-- ==========================
             Navigation
             ========================== -->

        <nav class="link-container">

            <a href="index.html">
                Home
            </a>

            <a href="projects.html">
                My Projects
            </a>

        </nav>


    </main>

</body>

</html>
"""

    BLOG_INDEX.write_text(
        page,
        encoding="utf-8"
    )

    print("✓ Built main blog page")


# ============================================================
# Build entire blog
# ============================================================

def build_blog():
    """
    Discover every blog directory containing post.md,
    build every article, and rebuild blog.html.
    """

    print("\nBuilding blog...\n")

    post_directories = []

    # --------------------------------------------------------
    # Discover posts
    # --------------------------------------------------------

    for directory in BLOG_DIRECTORY.iterdir():

        if not directory.is_dir():
            continue

        if not (directory / "post.md").exists():
            continue

        post_directories.append(directory)

    # --------------------------------------------------------
    # Sort newest -> oldest
    # --------------------------------------------------------

    def post_date(directory):

        post = load_post(directory)

        value = post.get("date")

        if isinstance(value, datetime):
            return value

        if isinstance(value, date):
            return datetime.combine(
                value,
                datetime.min.time()
            )

        try:
            return datetime.strptime(
                str(value),
                "%Y-%m-%d"
            )

        except (ValueError, TypeError):
            return datetime.min


    post_directories.sort(
        key=post_date,
        reverse=True
    )

    # --------------------------------------------------------
    # Build posts
    # --------------------------------------------------------

    for directory in post_directories:
        build_post(directory)

    # --------------------------------------------------------
    # Build blog homepage
    # --------------------------------------------------------

    build_blog_index(post_directories)

    print(
        f"\nFinished! Built "
        f"{len(post_directories)} post(s).\n"
    )


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    build_blog()