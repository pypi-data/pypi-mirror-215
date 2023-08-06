# Configuration file for Pelidoc using Pelican configuration format

from datetime import date
from pathlib import Path

# We are including a theme; override it if you want to go Pelican native
THEME = str(Path(__file__).parent / 'theme')

CURRENT_YEAR = date.today().strftime("%Y")

PATH = 'docs'

TIMEZONE = 'America/Vancouver'

DEFAULT_LANG = 'en'

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# LINKS = (('Pelican', 'https://getpelican.com/'),
#          ('Python.org', 'https://www.python.org/'),
#          ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
#          ('You can modify those links in your config file', '#'),)


# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Modified version of the Bootstrap3 theme puts the navigation in the sidebar

# MENUITEMS = [("Documentation","/documentation")]
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
CATEGORY_URL = "category/{slug}.html"
USE_FOLDER_AS_CATEGORY = True
