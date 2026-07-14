from cms.toolbar_pool import toolbar_pool

from cms_helpers.cms_toolbars import PageContentExtensionToolbar

from .models import ExtensionModel


@toolbar_pool.register
class ExtensionToolbar(PageContentExtensionToolbar):
    model = ExtensionModel
    insert_after = 'Advanced settings'
