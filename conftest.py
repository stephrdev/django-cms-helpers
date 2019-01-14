import pytest


def pytest_report_header(config):
    try:
        import anylink  # noqa
        anylink_present = True
    except ImportError:
        anylink_present = False

    try:
        import filer  # noqa
        filer_present = True
    except ImportError:
        filer_present = False

    if not anylink_present:
        return (
            'WARNING: django-anylink is not installed - some of the tests will '
            'be skipped.')
    if not filer_present:
        return (
            'WARNING: django-filer is not installed - some of the tests will '
            'be skipped.')


def pytest_collection_modifyitems(config, items):
    try:
        import anylink  # noqa
        anylink_present = True
    except ImportError:
        anylink_present = False

    try:
        import filer  # noqa
        filer_present = True
    except ImportError:
        filer_present = False

    if anylink_present and filer_present:
        return

    skip_anylink_tests = pytest.mark.skip(
        reason='django-anylink is not installed')
    skip_filer_tests = pytest.mark.skip(
        reason='django-filer is not installed')

    for item in items:
        if not anylink_present and 'anylink' in item.keywords:
            item.add_marker(skip_anylink_tests)
        if not filer_present and 'filer' in item.keywords:
            item.add_marker(skip_filer_tests)
