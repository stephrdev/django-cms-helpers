import os
import tempfile


DEBUG = True

SECRET_KEY = 'test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'menus',
    'cms',
    'treebeard',
    'cms_helpers',
    'tests.resources.cmsapp',
]

SITE_ID = 1
LANGUAGES = (('en-us', 'en-us'),)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'resources', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
            ],
        },
    },
]

MIDDLEWARE = MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
]

CMS_TOOLBARS = [
    'cms.cms_toolbars.PlaceholderToolbar',
    'cms.cms_toolbars.BasicToolbar',
    'cms.cms_toolbars.PageToolbar',
    'tests.resources.cmsapp.cms_toolbars.ExtensionToolbar',
]

ROOT_URLCONF = 'tests.urls'
CMS_TEMPLATES = (('empty_template.html', 'empty'),)

MEDIA_ROOT = tempfile.mkdtemp()
MEDIA_URL = '/media/'

try:
    import anylink  # noqa

    INSTALLED_APPS += ['anylink']
    ANYLINK_EXTENSIONS = (
        'anylink.extensions.ExternalLink',
        'cms_helpers.anylink_extensions.CmsPageLink',
    )
except ImportError:
    pass

try:
    import filer  # noqa

    INSTALLED_APPS += ['mptt', 'easy_thumbnails', 'filer']
except ImportError:
    pass

CMS_HELPERS_PAGE_TITLEEXTENSION_CACHE = True
