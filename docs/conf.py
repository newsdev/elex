#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# Path munging
sys.path.insert(0, os.path.abspath('..'))
import elex  # NOQA

# Extensions
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx']
autodoc_member_order = 'bysource'

intersphinx_mapping = {
    'python': ('http://docs.python.org/3.6', None)
}

# Templates
templates_path = ['_templates']
master_doc = 'index'

# Metadata
project = u'elex'
copyright = u'2015-2018, New York Times & NPR'
version = elex.__version__
release = elex.__version__

exclude_patterns = ['_build']
pygments_style = 'sphinx'

# HTMl theming
html_theme = 'default'

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

htmlhelp_basename = 'elexdoc'

# Ignore warnings for the GitHub README badges
suppress_warnings = ['image.nonlocal_uri']
