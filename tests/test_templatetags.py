from unittest import mock

import pytest
from cms.api import create_page, publish_page
from django.contrib.auth.models import User
from django.core.cache import cache
from django.template import Context, Template

from tests.resources.cmsapp.models import ExtensionModel


@pytest.mark.django_db
class TestPageTitleExtensionTemplateTag:

    @pytest.fixture(autouse=True, scope="function")
    def _django_clear_cache(self):
        cache.clear()

    @mock.patch('cms_helpers.templatetags.cms_helpers.Page.objects.get')
    def test_no_cms(self, page_mock, rf):
        page_mock.side_effect = NameError
        template = Template(
            '{% load cms_helpers %}{% page_titleextension 1 "extensionmodel" %}')
        context = Context({'request': rf.get('/')})
        with pytest.raises(ImportError):
            assert template.render(context) == ''

    def test_page_not_found(self, rf):
        template = Template(
            '{% load cms_helpers %}{% page_titleextension 1 "extensionmodel" %}')
        context = Context({'request': rf.get('/')})
        assert template.render(context) == 'None'

    def test_no_page(self, rf):
        request = rf.get('/')
        request.user = User()
        page = create_page('Test Page', 'INHERIT', 'en-us')
        template = Template((
            '{%% load cms_helpers %%}'
            '{%% page_titleextension %s "extensionmodel" %%}'
        ) % page.pk)
        context = Context({'request': request})
        assert template.render(context) == 'None'

    def test_extension_not_found(self, rf):
        request = rf.get('/')
        request.user = User.objects.create(username='admin', is_superuser=True)

        page = create_page('Test Page', 'INHERIT', 'en-us')
        publish_page(page, request.user, 'en-us')
        page.refresh_from_db()

        template = Template((
            '{%% load cms_helpers %%}'
            '{%% page_titleextension %s "extensionmodel" %%}'
        ) % page.pk)
        context = Context({'request': request})
        assert template.render(context) == 'None'

    def test_extension_found_public(self, rf):
        request = rf.get('/')
        request.user = User.objects.create(username='admin', is_superuser=True)

        page = create_page('Test Page', 'INHERIT', 'en-us')
        publish_page(page, request.user, 'en-us')
        page.refresh_from_db()

        ExtensionModel.objects.create(
            extended_object=page.get_public_object().get_title_obj(), name='public')
        ExtensionModel.objects.create(
            extended_object=page.get_draft_object().get_title_obj(), name='draft')

        template = Template((
            '{%% load cms_helpers %%}'
            '{%% page_titleextension %s "extensionmodel" %%}'
        ) % page.pk)
        context = Context({'request': request})
        assert template.render(context) == 'public'

    def test_extension_found_draft(self, rf):
        request = rf.get('/')
        request.user = User.objects.create(username='admin', is_staff=True, is_superuser=True)
        request.session = {'cms_edit': True}

        page = create_page('Test Page', 'INHERIT', 'en-us')
        publish_page(page, request.user, 'en-us')
        page.refresh_from_db()

        ExtensionModel.objects.create(
            extended_object=page.get_public_object().get_title_obj(), name='public')
        ExtensionModel.objects.create(
            extended_object=page.get_draft_object().get_title_obj(), name='draft')

        template = Template((
            '{%% load cms_helpers %%}'
            '{%% page_titleextension %s "extensionmodel" %%}'
        ) % page.pk)
        context = Context({'request': request})
        assert template.render(context) == 'draft'

    def test_extension_found_performance(self, rf, django_assert_num_queries):
        request = rf.get('/')
        request.user = User.objects.create(username='admin', is_superuser=True)

        page = create_page('Test Page', 'INHERIT', 'en-us')
        publish_page(page, request.user, 'en-us')
        page.refresh_from_db()

        ExtensionModel.objects.create(
            extended_object=page.get_public_object().get_title_obj(), name='public')
        context = Context({'request': request})

        template = Template((
            '{%% load cms_helpers %%}'
            '{%% page_titleextension %s "extensionmodel" %%}'
        ) % page.pk)
        info = (
            '1 query get draft page, '
            '1 query get public page, '
            '1 query get title, '
            '1 query get extension'
        )
        with django_assert_num_queries(4, info=info):
            assert template.render(context) == 'public'
        # Rendering another time should be cached and not hit the DB
        with django_assert_num_queries(0, info=info):
            assert template.render(context) == 'public'
