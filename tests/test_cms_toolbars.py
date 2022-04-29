from unittest import mock

import pytest
from cms.api import create_page, create_title
from cms.toolbar.items import ModalItem, SubMenu

from tests.resources.cmsapp.models import ExtensionModel


def test_titleextensiontoolbar_inserted(admin_client):
    page = create_page('Test Page', 'INHERIT', 'en-us')

    response = admin_client.get('{0}?edit=on'.format(page.get_absolute_url()))
    toolbar = response.context['request'].toolbar
    menu = toolbar.get_menu('page')
    item = menu.items[5]
    assert isinstance(item, ModalItem)
    assert item.name == 'Extension...'
    assert item.url.startswith('/admin/cmsapp/extensionmodel/')


@mock.patch('cms_helpers.cms_toolbars.TitleExtensionToolbar.get_item_position')
def test_titleextensiontoolbar_not_inserted(position_mock, admin_client):
    response = admin_client.get('/non-cms/')
    toolbar = response.context['request'].toolbar
    assert toolbar.get_menu('page') is None
    assert position_mock.called is False


@pytest.mark.django_db
class TestTitleextensiontoolbarMultilingual:

    @pytest.fixture(autouse=True)
    def setup(self, settings):
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

    def test_add(self, admin_client):
        page = create_page('Test Page', 'INHERIT', 'en-us')
        title_de = create_title(language='de', page=page, title='Test Page de')
        title_en = page.get_title_obj(language='en-us')
        expected_url = '/admin/cmsapp/extensionmodel/add/?extended_object={0}'

        response = admin_client.get(
            '{0}?edit=on'.format(page.get_absolute_url('de')))
        toolbar = response.context['request'].toolbar
        menu = toolbar.get_menu('page')
        item = menu.items[5]
        extensions = {ext.name: ext for ext in item.items}

        assert isinstance(item, SubMenu)
        assert item.name == 'Extension'
        assert len(item.items) == 2
        assert 'English Extension...' in extensions
        assert 'German Extension...' in extensions
        assert extensions['English Extension...'].url == (
            expected_url.format(title_en.pk))
        assert extensions['German Extension...'].url == (
            expected_url.format(title_de.pk))

    def test_change(self, admin_client):
        page = create_page('Test Page', 'INHERIT', 'en-us')
        title_de = create_title(
            language='de', page=page, title='Test Page de')
        title_en = page.get_title_obj(language='en-us')
        extension_de = ExtensionModel.objects.create(
            name='de', extended_object=title_de)
        extension_en = ExtensionModel.objects.create(
            name='en', extended_object=title_en)
        expected_url = '/admin/cmsapp/extensionmodel/{0}/change/'

        response = admin_client.get(
            '{0}?edit=on'.format(page.get_absolute_url('de')))
        toolbar = response.context['request'].toolbar
        menu = toolbar.get_menu('page')
        item = menu.items[5]
        extensions = {ext.name: ext for ext in item.items}

        assert extensions['English Extension...'].url == (
            expected_url.format(extension_en.pk))
        assert extensions['German Extension...'].url == (
            expected_url.format(extension_de.pk))

    def test_add_change(self, admin_client):
        page = create_page('Test Page', 'INHERIT', 'en-us')
        title_de = create_title(language='de', page=page, title='Test Page de')
        title_en = page.get_title_obj(language='en-us')
        extension_de = ExtensionModel.objects.create(
            name='de', extended_object=title_de)
        expected_url_add = (
            '/admin/cmsapp/extensionmodel/add/?extended_object={0}')
        expected_url_change = '/admin/cmsapp/extensionmodel/{0}/change/'

        response = admin_client.get(
            '{0}?edit=on'.format(page.get_absolute_url('de')))
        toolbar = response.context['request'].toolbar
        menu = toolbar.get_menu('page')
        item = menu.items[5]
        extensions = {ext.name: ext for ext in item.items}

        assert extensions['English Extension...'].url == (
            expected_url_add.format(title_en.pk))
        assert extensions['German Extension...'].url == (
            expected_url_change.format(extension_de.pk))

    def test_change_add(self, admin_client):
        page = create_page('Test Page', 'INHERIT', 'en-us')
        title_de = create_title(language='de', page=page, title='Test Page de')
        title_en = page.get_title_obj(language='en-us')
        extension_en = ExtensionModel.objects.create(
            name='en', extended_object=title_en)
        expected_url_add = (
            '/admin/cmsapp/extensionmodel/add/?extended_object={0}')
        expected_url_change = '/admin/cmsapp/extensionmodel/{0}/change/'

        response = admin_client.get(
            '{0}?edit=on'.format(page.get_absolute_url('de')))
        toolbar = response.context['request'].toolbar
        menu = toolbar.get_menu('page')
        item = menu.items[5]
        extensions = {ext.name: ext for ext in item.items}

        assert extensions['English Extension...'].url == (
            expected_url_change.format(extension_en.pk))
        assert extensions['German Extension...'].url == (
            expected_url_add.format(title_de.pk))
