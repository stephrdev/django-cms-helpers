Changelog
=========

3.0.0 (unreleased)
------------------

See ``docs/migration.rst`` for a step-by-step upgrade guide from 2.x.

* Add support for django CMS 4.1 and require ``djangocms-versioning>=2.0``
* Drop support for django CMS < 4.1 (django CMS 3.x is no longer supported, use 2.x)
* Drop support for Django < 4.2, Python < 3.10
* ``TitleExtensionToolbar`` renamed to ``PageContentExtensionToolbar``, following
  core's ``TitleExtension`` -> ``PageContentExtension`` rename
* ``{% page_titleextension %}`` template tag renamed to ``{% page_content_extension %}``;
  it now shows the draft version while editing/previewing (via
  ``djangocms-versioning``) and the published version otherwise
* ``CMS_HELPERS_PAGE_TITLEEXTENSION_CACHE`` setting renamed to
  ``CMS_HELPERS_PAGE_CONTENT_EXTENSION_CACHE``
* ``CmsPageLink``'s ``PageField`` now declares an explicit ``related_name``
  (was previously unset), required by ``djangocms-4-migration`` for projects
  migrating an existing django CMS 3 database


2.0.0 (2023-02-07)
------------------

* Add support for Django 4.1 and django-cms 3.11
* Drop support for Django < 3.2
* Drop support for django-cms < 3.9


1.0.0 (2022-04-29)
------------------

* Drop support for Django < 2.2
* Drop support for django-cms < 3.7
* Drop support for Python < 3.8
* Add support for Django 3.2, django-cms 3.10


0.3.0 (2020-09-29)
------------------

* Add caching for page_titleextension template tag


0.2.0 (2019-04-30)
------------------

* Add support for multiple languages to TitleExtensionToolbar
* Fix support for multi-domain links in django-cms 3.6


0.1.0 (2019-03-20)
------------------

* Add compatibility with django 2 and django-cms 3.6


0.0.1 (2019-02-07)
------------------

* Initial release of `django-cms-helpers`
