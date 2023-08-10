# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os
import subprocess

sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('.'))

try:
    # Run the 'pip list' command and capture the output
    result = subprocess.run(['pip', 'list'], stdout=subprocess.PIPE, text=True, check=True)
    output = result.stdout

    # Split the output into lines and ignore the header
    lines = output.strip().split('\n')[2:]

    # Extract package names from each line
    packages = [line.split()[0] for line in lines]

    print(packages)
except subprocess.CalledProcessError as e:
    print("Error:", e)


import pythonparts as pp

print(pp.create_scene('Hello'))

print('SYYYYS', sys.path)


import os

def list_folders(directory):
    try:
        # Get a list of all entries in the directory
        entries = os.listdir(directory)

        # Filter out only the directories
        folders = [entry for entry in entries if os.path.isdir(os.path.join(directory, entry))]

        return folders
    except OSError as e:
        print("Error:", e)
        return []

for path in sys.path:
    target_directory = path
    folders = list_folders(target_directory)

    print("List of folders in", target_directory)
    for folder in folders:
        print(folder)



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
