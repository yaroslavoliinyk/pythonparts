# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os


sys.path.insert(0, os.path.abspath('../'))
print('SYYYYS', sys.path)
sys.path.insert(0, os.path.abspath('../../'))


project = 'Pythonparts'
copyright = '2023, Yaroslav Oliinyk'
author = 'Yaroslav Oliinyk'
release = '0.1.1'
autodoc_member_order = 'bysource'
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.duration',
              'sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_logo = 'images/logo.jpg'
html_theme = 'furo'
html_static_path = ['_static']
