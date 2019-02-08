Usage
=====

page_titleextension templatetag
-------------------------------

To obtain cms page title extension object in template use
page_titleextension templatetag. The tag requires cms page id
and name of extension model.


.. code-block:: text

    {% load cms_helpers %}

    {% page_titleextension 1 "extensionmodel" %}


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


cms title extension toolbar
---------------------------

TitleExtensionToolbar provides boilerplate code for your ExtensionToolbar model.
It includes populate function and enables setting the position
of the extension in the menu through insert_after parameter.


.. code-block:: python

    from cms.extensions import TitleExtension
    from cms.extensions.extension_pool import extension_pool
    from cms.toolbar_pool import toolbar_pool
    from cms_helpers.cms_toolbars import TitleExtensionToolbar


    @extension_pool.register
    class YourExtensionModel(TitleExtension):
        name = models.CharField(max_length=255)

        class Meta:
            verbose_name = 'yourExtension'


    @toolbar_pool.register
    class ExtensionToolbar(TitleExtensionToolbar):
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
