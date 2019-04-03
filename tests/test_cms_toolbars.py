from unittest import mock

from cms.api import create_page
from cms.toolbar.items import ModalItem, SubMenu


def test_titleextensiontoolbar_inserted(admin_client):
    page = create_page('Test Page', 'INHERIT', 'en-us')

    response = admin_client.get('{0}?edit=on'.format(page.get_absolute_url()))
    toolbar = response.context['request'].toolbar
    menu = toolbar.get_menu('page')
    item = menu.items[5]
    assert isinstance(item, ModalItem)
    assert item.name == 'Extension...'
    assert item.url.startswith('/admin/cmsapp/extensionmodel/')


def test_titleextensiontoolbar_inserted_multilang(admin_client, settings):
    settings.LANGUAGE_CODE = 'en-us'
    settings.USE_I18N = True
    settings.USE_L10N = True
    settings.LANGUAGES = [
        ('en-us', 'English'),
        ('de', 'German'),
    ]
    settings.CMS_LANGUAGES = {
        1: [
            {'code': 'de', 'name': 'German'},
            {'code': 'en-us', 'name': 'English'},
        ]
    }

    page = create_page('Test Page', 'INHERIT', 'en-us')
    response = admin_client.get('{0}?edit=on'.format(page.get_absolute_url()))
    toolbar = response.context['request'].toolbar
    menu = toolbar.get_menu('page')
    item = menu.items[5]
    assert isinstance(item, SubMenu)
    assert item.name == 'Extension'
    assert len(item.items) == 1
    assert item.items[0].name == 'English Extension...'
    assert item.items[0].url.startswith('/admin/cmsapp/extensionmodel/')


@mock.patch('cms_helpers.cms_toolbars.TitleExtensionToolbar.get_item_position')
def test_titleextensiontoolbar_not_inserted(position_mock, admin_client):
    response = admin_client.get('/non-cms/')
    toolbar = response.context['request'].toolbar
    assert toolbar.get_menu('page') is None
    assert position_mock.called is False
