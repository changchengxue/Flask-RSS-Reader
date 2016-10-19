import os

basedir =os.path.abspath(os.path.dirname(__file__))

SITE_TITLE = 'bookmarks'
CSRF_ENABLED = True
SECRET_KEY = 'chang-cheng-xue'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flaskmarks.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

CAN_REGISTER = True
# ITEMS_PER_PAGE = 15
# SUGGESTIONS = True
SUGGESTIONS_COUNT = 1
# RECENTLY_ADDED = 2
# RECENTLY = True
# EXTRA_BOX = True
SITE_FOOTER = 'Bookmark and RSS feeder Copyright © 2016 changcheng'
