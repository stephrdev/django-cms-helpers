Installation
============

* Install with pip::

    pip install django-cms-helpers


* Your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # ...
        'anylink',
        'cms',
        'filer',

        'cms_helpers',
    )


* To use ``CmsPageLink`` anylink extension add to your settings::

    ANYLINK_EXTENSIONS = (
        # ...

        'cms_helpers.anylink_extensions.CmsPageLink',
    )
