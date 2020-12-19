
import os
import sys
import django


sys.path.insert(0, os.path.abspath('/app'))
os.environ.setdefault('DATABASE_URL', '')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'alabaster'
