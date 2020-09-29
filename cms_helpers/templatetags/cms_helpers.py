from cms.cache import _get_cache_key
from cms.models import Page, get_cms_setting
from cms.utils.moderator import use_draft
from django import template
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import get_language


register = template.Library()

NO_EXTENSION = 'no_extension'


@register.simple_tag(takes_context=True)
def page_titleextension(context, page_id, extension):
    request = context.get('request')
    is_draft = request and hasattr(request, 'user') and use_draft(request)
    lang = get_language()
    site_id = settings.SITE_ID
    page_cache_key = _get_cache_key('page_titleextension', page_id, lang, site_id)
    cache_key = '{}_{}_{}'.format(page_cache_key, is_draft, extension)

    cached = cache.get(cache_key)
    if cached:
        if cached == NO_EXTENSION:
            return None
        return cached

    try:
        page = Page.objects.get(pk=page_id)
        if is_draft:
            page = page.get_draft_object()
        else:
            page = page.get_public_object()
    except NameError:
        raise ImportError(
            'django-cms is required when using page_titleextension tag')
    except Page.DoesNotExist:
        return None

    if not page:
        return None

    try:
        title_extension = getattr(page.get_title_obj(), extension)
    except ObjectDoesNotExist:
        cache.set(cache_key, NO_EXTENSION, get_cms_setting('CACHE_DURATIONS')['content'])
        return None
    else:
        cache.set(cache_key, title_extension, get_cms_setting('CACHE_DURATIONS')['content'])
        return title_extension
