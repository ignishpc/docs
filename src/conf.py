# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys
import datetime
sys.path.insert(0, os.path.abspath('.'))
_today = datetime.datetime.now()


# -- Project information -----------------------------------------------------
package = 'ignishpc'
project = 'IgnisHPC'
release = '2.0'
version = '2.0.0'
authors = ['César Piñeiro', 'Juan C. Pichel']
copyright = f'{_today.year}, {", ".join(authors)}'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
default_role = 'any'
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']


# -- Options for HTML output -------------------------------------------------
# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
try:
    import sphinx_rtd_theme
except ImportError:
    sphinx_rtd_theme = None

html_theme = (
    'sphinx_rtd_theme' if sphinx_rtd_theme is not None else 'default'
)
html_logo = "_static/img/ignis-hpc-small.svg"
html_favicon = '_static/img/favicon.ico'
html_theme_options = {
    'logo_only': False,
    'display_version': False,
}

if html_theme == 'default':
    html_copy_source = False

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
if sphinx_rtd_theme is not None:
    html_css_files = ['css/custom.css',]


# -- Options for HTMLHelp output ------------------------------------------
htmlhelp_basename = f'{package}-man'


# -- Options for LaTeX output ---------------------------------------------

# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    ('index', f'{package}.tex', project, " and ".join(authors), 'howto'),
]

latex_elements = {
    'papersize': 'a4',
}


# -- Options for manual page output ---------------------------------------

# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', package, project, authors, 1)
]


# -- Options for Texinfo output -------------------------------------------

# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ('index', package, project, "@*".join(authors),
     package, f'{project}.', 'Miscellaneous'),
]


# -- Options for Epub output ----------------------------------------------

# Output file base name for ePub builder.
epub_basename = package

# Suppress "WARNING: unknown mimetype for ..." when building EPUB.
suppress_warnings = ["epub.unknown_project_files"]
