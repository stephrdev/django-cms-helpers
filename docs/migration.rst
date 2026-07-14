Migrating to 3.0 (django CMS 4)
===============================

django-cms-helpers 3.0 drops support for django CMS 3.x and targets django CMS 4.1
with `djangocms-versioning <https://github.com/django-cms/djangocms-versioning>`_.
This is a breaking release: django CMS 4 renamed several core APIs and removed
draft/publish from the core, and django-cms-helpers 3.0 follows those renames
rather than papering over them with compatibility shims.

If you are still on django CMS 3.x, stay on django-cms-helpers 2.x — it continues
to work there and is not going away. Only move to 3.0 once your project itself has
moved to django CMS 4.1.

This guide only covers the django-cms-helpers side of that move. For the django CMS
core upgrade itself (versioning, the Page/PageContent split, placeholders, the
``djangocms-4-migration`` tool for migrating an existing database), see the
`django CMS 4 upgrade guide <https://docs.django-cms.org/en/latest/upgrade/4.0.html>`_
first — do that part before touching django-cms-helpers.


1. Add djangocms-versioning
----------------------------

django-cms-helpers 3.0 requires ``djangocms-versioning`` and assumes it is installed;
it is no longer optional.

.. code-block:: python

    INSTALLED_APPS = (
        # ...
        'cms',
        'djangocms_versioning',

        'cms_helpers',
    )


2. Rename ``TitleExtensionToolbar``
------------------------------------

``TitleExtensionToolbar`` was renamed to ``PageContentExtensionToolbar``, following
core's own ``TitleExtension`` -> ``PageContentExtension`` rename.

.. code-block:: diff

    - from cms_helpers.cms_toolbars import TitleExtensionToolbar
    + from cms_helpers.cms_toolbars import PageContentExtensionToolbar

      @toolbar_pool.register
    - class ExtensionToolbar(TitleExtensionToolbar):
    + class ExtensionToolbar(PageContentExtensionToolbar):
          model = YourExtensionModel
          insert_after = 'Advanced settings'

While you're there, your extension model itself needs the matching core rename
(this part is django CMS, not django-cms-helpers, but you'll hit it in the same
place):

.. code-block:: diff

    - from cms.extensions import TitleExtension, TitleExtensionAdmin
    + from cms.extensions import PageContentExtension, PageContentExtensionAdmin

    - class YourExtensionModel(TitleExtension):
    + class YourExtensionModel(PageContentExtension):
          ...

    - admin.site.register(YourExtensionModel, TitleExtensionAdmin)
    + admin.site.register(YourExtensionModel, PageContentExtensionAdmin)

Run ``makemigrations`` for the app that owns ``YourExtensionModel`` afterwards —
the base class swap changes the FK target from ``Title`` to ``PageContent`` and
needs a migration, even though no data actually needs moving if you're already
migrating from a fresh django CMS 4 install.


3. Rename the template tag
-----------------------------

``{% page_titleextension %}`` was renamed to ``{% page_content_extension %}``.

.. code-block:: diff

    {% load cms_helpers %}

    - {% page_titleextension 1 "extensionmodel" %}
    + {% page_content_extension 1 "extensionmodel" %}

Its behavior also changed slightly: previously it used django CMS 3's built-in
``use_draft``/session-flag mechanism to decide between draft and public content.
It now shows the draft version whenever the current request's toolbar is in edit
or preview mode (via ``djangocms-versioning``), and the published version
otherwise. For the common case — showing published content on the live site,
draft while editing in the toolbar — this behaves the same as before; only a
request forcing draft mode through means other than the toolbar (e.g. a raw
session flag) would previously have seen draft content and now won't.

If you set the cache override setting, rename it too:

.. code-block:: diff

    - CMS_HELPERS_PAGE_TITLEEXTENSION_CACHE = False
    + CMS_HELPERS_PAGE_CONTENT_EXTENSION_CACHE = False


4. Check ``CmsPageLink`` usages
----------------------------------

``CmsPageLink``'s ``PageField`` now declares an explicit ``related_name`` (it was
previously unset, i.e. Django's default). This has no effect on your data, but:

* If your project uses `djangocms-4-migration
  <https://github.com/django-cms/djangocms-4-migration>`_ to migrate an existing
  django CMS 3 database, that tool **requires** a real ``related_name`` on
  ``PageField`` usages (it explicitly rejects ``related_name="+"``, and an unset
  related name resolves to one that isn't guaranteed unique across models using
  the extension). Upgrade django-cms-helpers before running that migration, not
  after.
* Run ``makemigrations`` for any app that uses ``anylink.extensions.BaseLink``
  models with the ``CmsPageLink`` extension — the related name change is a
  state-only migration (no schema/SQL changes), but Django's migration
  autodetector will still want to record it.


5. Bump your own requirements
--------------------------------

django-cms-helpers 3.0 requires Python 3.10+, Django 4.2+, and django CMS 4.1+.
If your project's own ``pyproject.toml``/``setup.py`` pins older floors for these,
raise them alongside the django-cms-helpers upgrade.


Checklist
---------

#. Project itself is already running django CMS 4.1 (core upgrade done first).
#. ``djangocms_versioning`` added to ``INSTALLED_APPS``.
#. ``TitleExtensionToolbar`` → ``PageContentExtensionToolbar`` (and the
   corresponding core ``TitleExtension``/``TitleExtensionAdmin`` renames).
#. ``{% page_titleextension %}`` → ``{% page_content_extension %}``, and the
   cache setting renamed if you used it.
#. ``makemigrations`` run for extension models and any ``CmsPageLink`` usages.
#. Python/Django/django CMS floors bumped in your own project's requirements.
