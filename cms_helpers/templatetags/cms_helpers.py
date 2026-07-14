from cms.cache import _get_cache_key
from cms.models import Page, get_cms_setting
from django import template
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import get_language
from djangocms_versioning.helpers import get_latest_admin_viewable_content


register = template.Library()

NO_EXTENSION = 'no_extension'
CMS_HELPERS_PAGE_CONTENT_EXTENSION_CACHE = 'CMS_HELPERS_PAGE_CONTENT_EXTENSION_CACHE'


def is_caching_desired(do_cache):
    if do_cache is not None:
        return do_cache
    custom_setting = getattr(settings, CMS_HELPERS_PAGE_CONTENT_EXTENSION_CACHE, None)
    if custom_setting is not None:
        return custom_setting
    return get_cms_setting('PLUGIN_CACHE')


def is_editing(request):
    toolbar = getattr(request, 'toolbar', None)
    return bool(toolbar and (toolbar.edit_mode_active or toolbar.preview_mode_active))


def get_page_content(page, language, request):
    if is_editing(request):
        # Prefer the draft so editors/previewers see their unpublished changes.
        return get_latest_admin_viewable_content(page, language=language)
    return page.get_content_obj(language)


@register.simple_tag(takes_context=True)
def page_content_extension(context, page_id, extension, do_cache=None):
    do_cache = is_caching_desired(do_cache=do_cache)
    request = context.get('request')

    if do_cache:
        lang = get_language()
        site_id = settings.SITE_ID
        cache_duration = get_cms_setting('CACHE_DURATIONS')['content']
        page_cache_key = _get_cache_key('page_content_extension', page_id, lang, site_id)
        cache_key = '{}_{}_{}'.format(page_cache_key, is_editing(request), extension)

        cached = cache.get(cache_key)
        if cached:
            if cached == NO_EXTENSION:
                return None
            return cached

    try:
        page = Page.objects.get(pk=page_id)
    except Page.DoesNotExist:
        return None

    page_content = get_page_content(page, get_language(), request)
    if not getattr(page_content, 'pk', None):
        return None

    try:
        page_content_extension_obj = getattr(page_content, extension)
    except ObjectDoesNotExist:
        if do_cache:
            cache.set(cache_key, NO_EXTENSION, timeout=cache_duration)
        return None
    else:
        if do_cache:
            cache.set(cache_key, page_content_extension_obj, timeout=cache_duration)
        return page_content_extension_obj
