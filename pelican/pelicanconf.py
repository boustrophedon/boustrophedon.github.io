#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

from datetime import date

AUTHOR = 'Harry Stern'
SITENAME = 'recycled math'
SITEURL = 'http://localhost:8000'

THEME = 'minimalXY0'

PLUGIN_PATHS = ["plugins"]
PLUGINS = ['render_math', 'readtime']

PATH = 'posts'
OUTPUT_PATH = 'tmp'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# URL and HTML file paths
ARCHIVES_SAVE_AS = 'archive.html'
CATEGORIES_SAVE_AS = 'categories.html'
AUTHORS_SAVE_AS = 'about.html'


FEED_ALL_ATOM = 'feeds/all.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
CATEGORY_FEED_ATOM = None

DEFAULT_PAGINATION = 10

# MINIMALXY settings

MINIMALXY_START_YEAR = 2014
MINIMALXY_CURRENT_YEAR = date.today().year

# Author
AUTHOR_INTRO = u"hi I'm harry"
AUTHOR_DESCRIPTION = u"""
I'm a recent graduate of Rutgers University with degrees in math and computer science. Geometry, rendering, and topology are my favorite topics. I want to get better at data science and machine learning and their relationship with geometry and topology.
"""
AUTHOR_AVATAR = 'https://avatars.githubusercontent.com/u/936147?s=240'
AUTHOR_WEB = 'https://harrystern.net'

# Social
SOCIAL = (
    ('github', 'https://github.com/boustrophedon'),
    ('linkedin', 'https://www.linkedin.com/in/harry-stern-013920158/'),
)

# Menu
MENUITEMS = (
    ('About', '/' + AUTHORS_SAVE_AS),
    ('Archive', '/' + ARCHIVES_SAVE_AS),
)
