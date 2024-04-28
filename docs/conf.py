from pallets_sphinx_themes import get_version
from pallets_sphinx_themes import ProjectLink

project = "Blinker"
copyright = "2010 Jason Kirtland"
release, version = get_version("blinker", placeholder=None)

default_role = "code"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinxcontrib.log_cabinet",
    "pallets_sphinx_themes",
]
autodoc_member_order = "groupwise"
autodoc_typehints = "description"
autodoc_preserve_defaults = True
extlinks = {
    "issue": ("https://github.com/pallets-eco/blinker/issues/%s", "#%s"),
    "pr": ("https://github.com/pallets-eco/blinker/pull/%s", "#%s"),
}

html_theme = "flask"
html_theme_options = {"index_sidebar_logo": False}
html_context = {
    "project_links": [
        ProjectLink("PyPI Releases", "https://pypi.org/project/blinker/"),
        ProjectLink("Source Code", "https://github.com/pallets-eco/blinker/"),
        ProjectLink("Issue Tracker", "https://github.com/pallets-eco/blinker/issues/"),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html", "ethicalads.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html", "ethicalads.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html", "ethicalads.html"]}
html_static_path = ["_static"]
html_logo = "_static/blinker-named.png"
html_title = f"Blinker Documentation ({version})"
html_show_sourcelink = False
