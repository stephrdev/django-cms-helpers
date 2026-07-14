from unittest import mock

import pytest
from cms.api import create_page, create_page_content
from cms.toolbar.items import ModalItem, SubMenu
from cms.toolbar.utils import get_object_edit_url
from django.contrib.auth.models import User
from djangocms_versioning.helpers import get_latest_admin_viewable_content

from tests.resources.cmsapp.models import ExtensionModel


def test_extensiontoolbar_inserted(admin_client):
    user = User.objects.create(username='creator', is_staff=True, is_superuser=True)
    page = create_page('Test Page', 'INHERIT', 'en-us', created_by=user)
    page_content = get_latest_admin_viewable_content(page, language='en-us')

    response = admin_client.get(get_object_edit_url(page_content))
    toolbar = response.context['request'].toolbar
    menu = toolbar.get_menu('page')
    item = menu.items[5]
    assert isinstance(item, ModalItem)
    assert item.name == 'Extension...'
    assert item.url.startswith('/admin/cmsapp/extensionmodel/')


@mock.patch('cms_helpers.cms_toolbars.PageContentExtensionToolbar.get_item_position')
def test_extensiontoolbar_not_inserted(position_mock, admin_client):
    response = admin_client.get('/non-cms/')
    toolbar = response.context['request'].toolbar
    assert toolbar.get_menu('page') is None
    assert position_mock.called is False


@pytest.mark.django_db
class TestExtensiontoolbarMultilingual:
    @pytest.fixture(autouse=True)
    def setup_method(self, settings):
        settings.LANGUAGE_CODE = 'en-us'
        settings.USE_I18N = True
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
        user = User.objects.create(username='creator', is_staff=True, is_superuser=True)
        page = create_page('Test Page', 'INHERIT', 'en-us', created_by=user)
        page_content_de = create_page_content(
            language='de', title='Test Page de', page=page, created_by=user
        )
        page_content_en = get_latest_admin_viewable_content(page, language='en-us')
        expected_url = '/admin/cmsapp/extensionmodel/add/?extended_object={0}'

        response = admin_client.get(get_object_edit_url(page_content_de))
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
            expected_url.format(page_content_en.pk)
        )
        assert extensions['German Extension...'].url == (
            expected_url.format(page_content_de.pk)
        )

    def test_change(self, admin_client):
        user = User.objects.create(username='creator', is_staff=True, is_superuser=True)
        page = create_page('Test Page', 'INHERIT', 'en-us', created_by=user)
        page_content_de = create_page_content(
            language='de', title='Test Page de', page=page, created_by=user
        )
        page_content_en = get_latest_admin_viewable_content(page, language='en-us')
        extension_de = ExtensionModel.objects.create(name='de', extended_object=page_content_de)
        extension_en = ExtensionModel.objects.create(name='en', extended_object=page_content_en)
        expected_url = '/admin/cmsapp/extensionmodel/{0}/change/'

        response = admin_client.get(get_object_edit_url(page_content_de))
        toolbar = response.context['request'].toolbar
        menu = toolbar.get_menu('page')
        item = menu.items[5]
        extensions = {ext.name: ext for ext in item.items}

        assert extensions['English Extension...'].url == (expected_url.format(extension_en.pk))
        assert extensions['German Extension...'].url == (expected_url.format(extension_de.pk))

    def test_add_change(self, admin_client):
        user = User.objects.create(username='creator', is_staff=True, is_superuser=True)
        page = create_page('Test Page', 'INHERIT', 'en-us', created_by=user)
        page_content_de = create_page_content(
            language='de', title='Test Page de', page=page, created_by=user
        )
        page_content_en = get_latest_admin_viewable_content(page, language='en-us')
        extension_de = ExtensionModel.objects.create(name='de', extended_object=page_content_de)
        expected_url_add = '/admin/cmsapp/extensionmodel/add/?extended_object={0}'
        expected_url_change = '/admin/cmsapp/extensionmodel/{0}/change/'

        response = admin_client.get(get_object_edit_url(page_content_de))
        toolbar = response.context['request'].toolbar
        menu = toolbar.get_menu('page')
        item = menu.items[5]
        extensions = {ext.name: ext for ext in item.items}

        assert extensions['English Extension...'].url == (
            expected_url_add.format(page_content_en.pk)
        )
        assert extensions['German Extension...'].url == (
            expected_url_change.format(extension_de.pk)
        )

    def test_change_add(self, admin_client):
        user = User.objects.create(username='creator', is_staff=True, is_superuser=True)
        page = create_page('Test Page', 'INHERIT', 'en-us', created_by=user)
        page_content_de = create_page_content(
            language='de', title='Test Page de', page=page, created_by=user
        )
        page_content_en = get_latest_admin_viewable_content(page, language='en-us')
        extension_en = ExtensionModel.objects.create(name='en', extended_object=page_content_en)
        expected_url_add = '/admin/cmsapp/extensionmodel/add/?extended_object={0}'
        expected_url_change = '/admin/cmsapp/extensionmodel/{0}/change/'

        response = admin_client.get(get_object_edit_url(page_content_de))
        toolbar = response.context['request'].toolbar
        menu = toolbar.get_menu('page')
        item = menu.items[5]
        extensions = {ext.name: ext for ext in item.items}

        assert extensions['English Extension...'].url == (
            expected_url_change.format(extension_en.pk)
        )
        assert extensions['German Extension...'].url == (
            expected_url_add.format(page_content_de.pk)
        )
