from unittest import mock

import pytest
from cms.api import create_page
from django.contrib.auth.models import User
from django.core.cache import cache
from django.template import Context, Template
from djangocms_versioning.helpers import (
    get_latest_admin_viewable_content,
    get_version_for_content,
)

from tests.resources.cmsapp.models import ExtensionModel


def _publish(page, user, language='en-us'):
    content = get_latest_admin_viewable_content(page, language=language)
    version = get_version_for_content(content)
    version.publish(user)
    return content


@pytest.mark.django_db
class TestPageContentExtensionTemplateTag:
    @pytest.fixture(autouse=True, scope='function')
    def _django_clear_cache(self, settings):
        del settings.CMS_HELPERS_PAGE_CONTENT_EXTENSION_CACHE
        cache.clear()

    def test_page_not_found(self, rf):
        template = Template(
            '{% load cms_helpers %}{% page_content_extension 1 "extensionmodel" %}'
        )
        context = Context({'request': rf.get('/')})
        assert template.render(context) == 'None'

    def test_no_page_content(self, rf):
        request = rf.get('/')
        user = User.objects.create(username='creator', is_staff=True, is_superuser=True)
        page = create_page('Test Page', 'INHERIT', 'en-us', created_by=user)
        template = Template(
            ('{%% load cms_helpers %%}{%% page_content_extension %s "extensionmodel" %%}')
            % page.pk
        )
        context = Context({'request': request})
        # Page has a draft but nothing published yet, and this request is not editing.
        assert template.render(context) == 'None'

    def test_extension_not_found(self, rf):
        request = rf.get('/')
        user = User.objects.create(username='creator', is_staff=True, is_superuser=True)
        page = create_page('Test Page', 'INHERIT', 'en-us', created_by=user)
        _publish(page, user)

        template = Template(
            ('{%% load cms_helpers %%}{%% page_content_extension %s "extensionmodel" %%}')
            % page.pk
        )
        context = Context({'request': request})
        assert template.render(context) == 'None'

    def test_extension_found_public(self, rf):
        request = rf.get('/')
        user = User.objects.create(username='creator', is_staff=True, is_superuser=True)
        page = create_page('Test Page', 'INHERIT', 'en-us', created_by=user)
        published_content = _publish(page, user)
        draft_version = get_version_for_content(published_content).copy(created_by=user)

        ExtensionModel.objects.create(extended_object=published_content, name='public')
        ExtensionModel.objects.create(extended_object=draft_version.content, name='draft')

        template = Template(
            ('{%% load cms_helpers %%}{%% page_content_extension %s "extensionmodel" %%}')
            % page.pk
        )
        context = Context({'request': request})
        assert template.render(context) == 'public'

    def test_extension_found_draft(self, rf):
        request = rf.get('/')
        request.toolbar = mock.Mock(edit_mode_active=True, preview_mode_active=False)
        user = User.objects.create(username='creator', is_staff=True, is_superuser=True)
        page = create_page('Test Page', 'INHERIT', 'en-us', created_by=user)
        published_content = _publish(page, user)
        draft_version = get_version_for_content(published_content).copy(created_by=user)

        ExtensionModel.objects.create(extended_object=published_content, name='public')
        ExtensionModel.objects.create(extended_object=draft_version.content, name='draft')

        template = Template(
            ('{%% load cms_helpers %%}{%% page_content_extension %s "extensionmodel" %%}')
            % page.pk
        )
        context = Context({'request': request})
        assert template.render(context) == 'draft'

    def test_extension_found_performance(self, rf, django_assert_num_queries):
        request = rf.get('/')
        user = User.objects.create(username='creator', is_staff=True, is_superuser=True)
        page = create_page('Test Page', 'INHERIT', 'en-us', created_by=user)
        published_content = _publish(page, user)

        ExtensionModel.objects.create(extended_object=published_content, name='public')
        context = Context({'request': request})

        template = Template(
            ('{%% load cms_helpers %%}{%% page_content_extension %s "extensionmodel" %%}')
            % page.pk
        )
        with django_assert_num_queries(3):
            assert template.render(context) == 'public'
        # Rendering another time should be cached and not hit the DB
        with django_assert_num_queries(0):
            assert template.render(context) == 'public'

    @pytest.mark.parametrize(
        'cms_plugin_cache, cms_helper_cache, template_tag_cache_info, cached_used',
        [
            (True, None, '', True),
            (False, None, '', False),
            (True, True, '', True),
            (False, True, '', True),
            (True, False, '', False),
            (True, True, 'do_cache=True', True),
            (False, False, 'do_cache=True', True),
            (True, True, 'do_cache=False', False),
        ],
    )
    @mock.patch('cms_helpers.templatetags.cms_helpers.cache')
    def test_extension_found_cache(
        self,
        cache_mock,
        rf,
        settings,
        cms_plugin_cache,
        cms_helper_cache,
        template_tag_cache_info,
        cached_used,
    ):
        cache_mock.get.return_value = None
        if cms_plugin_cache is not None:
            settings.CMS_PLUGIN_CACHE = cms_plugin_cache
        if cms_helper_cache is not None:
            settings.CMS_HELPERS_PAGE_CONTENT_EXTENSION_CACHE = cms_helper_cache
        request = rf.get('/')
        user = User.objects.create(username='creator', is_staff=True, is_superuser=True)
        page = create_page('Test Page', 'INHERIT', 'en-us', created_by=user)
        published_content = _publish(page, user)

        ExtensionModel.objects.create(extended_object=published_content, name='public')
        context = Context({'request': request})

        template = Template(
            ('{%% load cms_helpers %%}{%% page_content_extension %s "extensionmodel" %s %%}')
            % (page.pk, template_tag_cache_info)
        )
        assert template.render(context) == 'public'
        assert cache_mock.get.called == cached_used
