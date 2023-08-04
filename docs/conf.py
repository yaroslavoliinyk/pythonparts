# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

# Add the path to your Python project
sys.path.insert(0, os.path.abspath('../'))

project = 'pythonparts'
copyright = '2023, yaroliinyk'
author = 'yaroliinyk'
release = 'yaroliinyk'
html_static_path = ['_static']
html_logo = '_static/logo.jpg'
html_css_files = ['custom.css']
html_theme = "sphinxdoc"


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
autodoc_mock_imports = ["public"]
autodoc_default_options = {
    'members': True,           # Document members (methods and attributes)
    'undoc-members': False,    # Exclude members without documentation
    'private-members': False,  # Exclude private members (those starting with an underscore)
    'special-members': False,  # Exclude special members (like __init__)
}

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.doctest',]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
