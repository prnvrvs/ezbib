import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'ezbib'
copyright = '2026, Pranav'
author = 'Pranav'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser',
    'sphinx_design',
    'sphinx_copybutton',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']

html_theme_options = {
    "github_url": "https://github.com/prnvrvs/ezbib",
    "repository_url": "https://github.com/prnvrvs/ezbib",
    "use_repository_button": True,
}

myst_enable_extensions = [
    "colon_fence",
    "html_image",
    "replacements",
    "smartquotes",
    "tasklist",
]
