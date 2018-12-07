import mock
import pytest
from cms.api import create_page, publish_page
from django.contrib.auth.models import User
from django.template import Context, Template

from tests.resources.cmsapp.models import ExtensionModel


@pytest.mark.django_db
class TestPageTitleExtensionTemplateTag:

    @mock.patch('cms_helpers.templatetags.page_titleextension.Page.objects.get')
    def test_no_cms(self, page_mock, rf):
        page_mock.side_effect = NameError
        template = Template(
            '{% load page_titleextension %}{% page_titleextension 1 "extensionmodel" %}')
        context = Context({'request': rf.get('/')})
        with pytest.raises(ImportError):
            assert template.render(context) == ''

    def test_page_not_found(self, rf):
        template = Template(
            '{% load page_titleextension %}{% page_titleextension 1 "extensionmodel" %}')
        context = Context({'request': rf.get('/')})
        assert template.render(context) == 'None'

    def test_no_page(self, rf):
        request = rf.get('/')
        request.user = User()
        page = create_page('Test Page', 'INHERIT', 'en-us')
        template = Template((
            '{%% load page_titleextension %%}'
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
            '{%% load page_titleextension %%}'
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
            '{%% load page_titleextension %%}'
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
            '{%% load page_titleextension %%}'
            '{%% page_titleextension %s "extensionmodel" %%}'
        ) % page.pk)
        context = Context({'request': request})
        assert template.render(context) == 'draft'
