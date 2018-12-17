from cms.toolbar_pool import toolbar_pool

from cms_helpers.cms_toolbars import TitleExtensionToolbar

from .models import ExtensionModel


@toolbar_pool.register
class ExtensionToolbar(TitleExtensionToolbar):
    model = ExtensionModel
    insert_after = 'Advanced settings'
