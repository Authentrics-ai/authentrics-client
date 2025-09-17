# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Authentrics Client"
copyright = "2025, Authentrics.ai"
author = "Authentrics.ai"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "agogo"
html_static_path = ["_static"]
html_theme_options = {
    # "bodyfont": "",
    # "headerfont": "",
    "pagewidth": "80em",
    "documentwidth": "50em",
    "sidebarwidth": "30em",
    "rightsidebar": "true",
    "bgcolor": "#47215C",
    "headerbg": "#47215C",
    "footerbg": "#47215C",
    "linkcolor": "#D984A3",
    # "headercolor1": "#47215C",
    "headercolor2": "#A65198",
    "headerlinkcolor": "#D984A3",
    # "textalign": "",
}

# Autodoc configuration
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
}
