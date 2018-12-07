import mock
import pytest
from django import forms
from filer.models import Image

from cms_helpers.filer_fields import AdminFileFormField

from .factories import ImageFactory


@pytest.mark.django_db
class TestAdminFileFormField:
    def test_super_not_clean(self):
        field = AdminFileFormField(
            mock.Mock(), Image.objects.all(), 'id', required=False)

        assert field.clean('') is None

    def test_without_alt_text_disabled(self):
        image = ImageFactory.create(default_alt_text=None)

        field = AdminFileFormField(
            mock.Mock(), Image.objects.all(), 'id', alt_text_required=False)
        assert isinstance(field.clean(str(image.pk)), Image)

    def test_without_alt_text_enabled(self):
        image = ImageFactory.create(default_alt_text=None)

        field = AdminFileFormField(mock.Mock(), Image.objects.all(), 'id')

        with pytest.raises(forms.ValidationError):
            field.clean(str(image.pk))

    def test_with_alt_text_enabled(self):
        image = ImageFactory.create(default_alt_text='Test')

        field = AdminFileFormField(mock.Mock(), Image.objects.all(), 'id')

        assert isinstance(field.clean(str(image.pk)), Image)

    def test_extensions_invalid_disabled(self):
        image = ImageFactory.create(default_alt_text='Test')

        field = AdminFileFormField(
            mock.Mock(), Image.objects.all(), 'id')

        assert isinstance(field.clean(str(image.pk)), Image)

    def test_extensions_valid_enabled(self):
        image = ImageFactory.create(default_alt_text='Test')

        field = AdminFileFormField(
            mock.Mock(), Image.objects.all(), 'id', extensions=['jpg', 'gif'])

        assert isinstance(field.clean(str(image.pk)), Image)

    def test_extensions_invalid_enabled(self):
        image = ImageFactory.create(default_alt_text='Test')

        field = AdminFileFormField(
            mock.Mock(), Image.objects.all(), 'id', extensions=['png', 'gif'])

        with pytest.raises(forms.ValidationError):
            field.clean(str(image.pk))
