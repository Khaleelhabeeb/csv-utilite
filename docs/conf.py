import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # Add parent directory to path for imports

# -- Project information -----------------------------------------------------

project = 'csv-utils'
copyright = '2024, CSV-UTILS(s)'
author = 'Khalil Habib Shariff'

# The short X.Y version
version = '1.0'
# The full version (including alpha/beta/rc tags)
release = '1.0'


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions shipped with Sphinx, or downloaded extensions.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',  # For docstrings with Google style
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.linkcode',  # Link source code to documentation
]


linkcode_base = os.path.abspath('..')  


napoleon_google_docstring = True
napoleon_numpy_docstring = True


templates_path = ['_templates']


source_suffix = '.rst'


master_doc = 'index'


exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



html_theme = 'sphinx_rtd_theme'  # Read the Docs theme


html_static_path = ['_static']


todo_include_todos = True



autodoc_default_flags = ['members', 'undoc-members', 'show-inheritance']


html_sidebars = {
    '**': [
        'relations.html',  
        'navigation.html',
        'searchbox.html',
        'donate.html',
    ]
}
