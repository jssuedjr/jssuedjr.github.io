from pathlib import Path
from datetime import date, datetime
import html

import frontmatter
import markdown

ROOT = Path(__file__).parent
PROJECTS_DIRECTORY = ROOT / "projects"
PROJECTS_INDEX = ROOT / "projects.html"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov"}


def format_date(value):
    if isinstance(value, (date, datetime)):
        return value.strftime("%B %d, %Y")
    if not value:
        return ""
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").strftime("%B %d, %Y")
    except (ValueError, TypeError):
        return str(value)


def load_project(project_directory):
    return frontmatter.load(project_directory / "project.md")


def discover_media(project_directory):
    media = []
    for subfolder in ("images", "videos"):
        folder = project_directory / subfolder
        if not folder.exists():
            continue
        for path in sorted(folder.iterdir()):
            if not path.is_file():
                continue
            suffix = path.suffix.lower()
            if suffix in IMAGE_EXTENSIONS or suffix in VIDEO_EXTENSIONS:
                media.append(path.relative_to(project_directory).as_posix())
    return media


def build_media_gallery(project_directory, project):
    configured = project.get("media", [])
    if isinstance(configured, str):
        configured = [configured]
    media = configured or discover_media(project_directory)
    if not media:
        return ""

    items = []
    for src in media:
        escaped = html.escape(str(src), quote=True)
        suffix = Path(str(src)).suffix.lower()
        if suffix in VIDEO_EXTENSIONS:
            items.append(f'''<figure class="project-media-item">
                <video controls preload="metadata">
                    <source src="{escaped}">
                    Your browser does not support embedded video.
                </video>
            </figure>''')
        else:
            items.append(f'''<figure class="project-media-item">
                <img src="{escaped}" alt="Project media for {html.escape(str(project.get('title', 'project')), quote=True)}" loading="lazy">
            </figure>''')

    return f'''<section class="project-media" aria-label="Project media">
        <div class="project-media-grid">
            {''.join(items)}
        </div>
    </section>'''


def build_pdf_section(project):
    pdf = project.get("pdf", "")
    if not pdf:
        return ""
    pdf_url = html.escape(str(pdf), quote=True)
    paper_title = html.escape(str(project.get("paper_title", "Project Report")))
    return f'''<section class="project-paper">
        <h2>{paper_title}</h2>
        <div class="pdf-embed">
            <iframe src="{pdf_url}" title="{paper_title}" loading="lazy"></iframe>
        </div>
        <p class="paper-actions">
            <a class="project-button" href="{pdf_url}" target="_blank" rel="noopener noreferrer">Open PDF</a>
            <a class="project-button" href="{pdf_url}" download>Download PDF</a>
        </p>
    </section>'''

def build_presentation_section(project):
    presentation = project.get("presentation", "")
    preview = project.get("presentation_preview", "")

    if not presentation and not preview:
        return ""

    title = html.escape(
        str(project.get("presentation_title", "Research Presentation"))
    )

    content = f'<section class="project-presentation"><h2>{title}</h2>'

    if preview:
        preview_url = html.escape(str(preview), quote=True)

        content += f'''
        <div class="pdf-embed">
            <iframe
                src="{preview_url}"
                title="{title}"
                loading="lazy">
            </iframe>
        </div>
        '''

    if presentation:
        presentation_url = html.escape(str(presentation), quote=True)

        content += f'''
        <p class="paper-actions">
            <a class="project-button"
               href="{presentation_url}"
               download>
                Download PowerPoint
            </a>
        </p>
        '''

    content += '</section>'
    return content


def build_project(project_directory):
    project = load_project(project_directory)
    title = project.get("title", "Untitled Project")
    summary = project.get("summary", "")
    project_date = format_date(project.get("date", ""))
    tools = project.get("tools", [])
    if isinstance(tools, str):
        tools = [item.strip() for item in tools.split(",") if item.strip()]

    body_html = markdown.markdown(project.content, extensions=["extra","toc","sane_lists","pymdownx.arithmatex",], extension_configs={"pymdownx.arithmatex": {"generic": True,}}
)
    media_html = build_media_gallery(project_directory, project)
    presentation_html = build_presentation_section(project)
    pdf_html = build_pdf_section(project)
    tools_html = ""
    if tools:
        tools_html = '''<section class="project-section">
            <h2>Methods &amp; Tools</h2>
            <div class="tool-list">''' + "".join(
                f'<span class="tool-tag">{html.escape(str(tool))}</span>' for tool in tools
            ) + "</div></section>"

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(str(title))} | Jaime Sued</title>
    <link rel="stylesheet" href="../../styles.css">
    <link rel="stylesheet" href="../../projects.css">
    <!-- MathJax configuration -->
    <script src="../../mathjax-config.js"></script>

    <!-- MathJax 4 -->
    <script
        id="MathJax-script"
        defer
        src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js">
    </script>
</head>
<body>
    <main class="project-page">
        <header class="project-header">
            <h1>{html.escape(str(title))}</h1>
            {f'<p class="project-date">{html.escape(project_date)}</p>' if project_date else ''}
        </header>

        {media_html}

        {f'''<section class="project-section project-summary">
            <h2>Project Summary</h2>
            <p>{html.escape(str(summary))}</p>
        </section>''' if summary else ''}

        <section class="project-section project-description">
            {body_html}
        </section>

        {tools_html}
        {pdf_html}
        {presentation_html}

        <nav class="project-navigation">
            <a href="../../projects.html">← Back to Projects</a>
        </nav>
    </main>
</body>
</html>
'''
    (project_directory / "index.html").write_text(page, encoding="utf-8")
    print(f"✓ Built project: {project_directory.name}")


def create_project_card(project_directory):
    project = load_project(project_directory)
    title = project.get("title", "Untitled Project")
    summary = project.get("summary", "")
    project_date = format_date(project.get("date", ""))
    folder = html.escape(project_directory.name, quote=True)

    thumbnail = project.get("thumbnail", "")
    thumb_html = ""
    if thumbnail:
        thumb_html = f'<img class="project-card-image" src="projects/{folder}/{html.escape(str(thumbnail), quote=True)}" alt="{html.escape(str(title), quote=True)} preview">'

    return f'''<article class="project-card">
        <a class="project-card-link" href="projects/{folder}/index.html">
            {thumb_html}
            <div class="project-card-body">
                <h2>{html.escape(str(title))}</h2>
                <p class="project-card-summary">{html.escape(str(summary))}</p>
                {f'<p class="project-card-date">{html.escape(project_date)}</p>' if project_date else ''}
            </div>
        </a>
    </article>'''


def build_projects_index(project_directories):
    cards = "\n".join(create_project_card(d) for d in project_directories)
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projects | Jaime Sued</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="projects.css">
</head>
<body>
    <main class="projects-content">
        <header class="projects-header">
            <h1>Projects</h1>
            <p>A selection of projects in machine learning, statistics, signal processing, quantitative modeling, and related areas.</p>
        </header>
        <section class="project-grid">
            {cards}
        </section>
        <nav class="link-container">
            <a href="index.html">Home</a>
            <a href="resume.pdf" target="_blank">Resume</a>
            <a href="https://www.github.com/jssuedjr" target="_blank" rel="noopener noreferrer">Github</a>
            <a href="blog.html">Math blog</a>
        </nav>
    </main>
</body>
</html>
'''
    PROJECTS_INDEX.write_text(page, encoding="utf-8")
    print("✓ Built main projects page")


def project_date(directory):
    value = load_project(directory).get("date")
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    try:
        return datetime.strptime(str(value), "%Y-%m-%d")
    except (ValueError, TypeError):
        return datetime.min


def build_projects():
    print("\nBuilding projects...\n")
    PROJECTS_DIRECTORY.mkdir(exist_ok=True)
    project_directories = [
        d for d in PROJECTS_DIRECTORY.iterdir()
        if d.is_dir() and (d / "project.md").exists()
    ]
    project_directories.sort(key=project_date, reverse=True)
    for directory in project_directories:
        build_project(directory)
    build_projects_index(project_directories)
    print(f"\nFinished! Built {len(project_directories)} project(s).\n")


if __name__ == "__main__":
    build_projects()
