Usage
=====

page_content_extension templatetag
-----------------------------------

To obtain a page content extension object in a template use the
page_content_extension templatetag. The tag requires the cms page id
and the name of the extension model. It shows the draft version of the
extension while editing/previewing the page in the toolbar (requiring
``djangocms-versioning``), and the published version otherwise.


.. code-block:: text

    {% load cms_helpers %}

    {% page_content_extension 1 "extensionmodel" %}


The page_content_extension templatetag is cached by default if
`CMS_PLUGIN_CACHE` is True, which is the default. You can override
globally by setting `CMS_HELPERS_PAGE_CONTENT_EXTENSION_CACHE = False`.
You can also override locally the template tag using the `do_cache`
keyword argument.


.. code-block:: text

    {% load cms_helpers %}

    {% page_content_extension 1 "extensionmodel" do_cache=False %}

anylink extension for cms pages
-------------------------------

To create links to cms pages with anylink library use CmsPageLink extension.
The extension needs to be added in settings. Details on how to use **anylink**
can be found `here <https://django-anylink.readthedocs.io/en/latest/>`_.


.. code-block:: python

    ANYLINK_EXTENSIONS = (
        ...

        'cms_helpers.anylink_extensions.CmsPageLink',
   )


cms page content extension toolbar
-----------------------------------

PageContentExtensionToolbar provides boilerplate code for your ExtensionToolbar model.
It includes populate function and enables setting the position
of the extension in the menu through insert_after parameter.


.. code-block:: python

    from cms.extensions import PageContentExtension
    from cms.extensions.extension_pool import extension_pool
    from cms.toolbar_pool import toolbar_pool
    from cms_helpers.cms_toolbars import PageContentExtensionToolbar


    @extension_pool.register
    class YourExtensionModel(PageContentExtension):
        name = models.CharField(max_length=255)

        class Meta:
            verbose_name = 'yourExtension'


    @toolbar_pool.register
    class ExtensionToolbar(PageContentExtensionToolbar):
        model = YourExtensionModel
        insert_after = 'Advanced settings'


filer field extension
---------------------

FilerFileField overwrites the native filer.fields.file.FilerFileField
and adds file extensions validation and sets default_alt_text
to required (with alt_text_required it can be also set to not required).


.. code-block:: python

    from cms_helpers.filer_fields import FilerFileField
    from django.db import models


    class YourModel(models.Model):
        your_file = FilerFileField(
            _('Your File'),
            extensions=('png', 'jpg', 'gif'),
            alt_text_required=False
        )
