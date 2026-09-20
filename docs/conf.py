import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'ezbib'
copyright = '2026, Pranav'
author = 'Pranav'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

myst_enable_extensions = [
    "colon_fence",
    "html_image",
    "replacements",
    "smartquotes",
    "tasklist",
]
