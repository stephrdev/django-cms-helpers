Installation
============

* Install with pip::

    pip install django-cms-helpers


* Your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # ...
        'cms',

        'cms_helpers',
    )


* To use ``CmsPageLink`` anylink extension install django-anylink
  and add to your settings::

    INSTALLED_APPS = (
        # ...
        'anylink',
    )

    ANYLINK_EXTENSIONS = (
        # ...

        'cms_helpers.anylink_extensions.CmsPageLink',
    )


* To use ``FilerFileField`` install django-filer and add to your settings::

    INSTALLED_APPS = (
        # ...
        'mptt',
        'easy_thumbnails',
        'filer'
    )
