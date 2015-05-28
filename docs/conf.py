#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from tuhinga import __version__ as tuhinga_version

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'tuhinga'
copyright = '2014-2015, Benjamin Althues'
version = tuhinga_version
release = tuhinga_version
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'nature'

man_pages = [
    ('index', 'tuhinga', 'tuhinga Documentation',
     ['Benjamin Althues'], 3)
]

texinfo_documents = [
    ('index', 'tuhinga', 'tuhinga Documentation',
     'Benjamin Althues', 'tuhinga', 'One line description of project.',
     'Miscellaneous'),
]
