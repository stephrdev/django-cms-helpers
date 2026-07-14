from cms.extensions import PageContentExtension
from cms.extensions.extension_pool import extension_pool
from django.db import models


try:
    from cms_helpers.filer_fields import FilerFileField
except ImportError:
    FilerFileField = None


@extension_pool.register
class ExtensionModel(PageContentExtension):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Extension'

    def __str__(self):
        return self.name


if FilerFileField:

    class FileModel(models.Model):
        file1 = FilerFileField(null=True)
        file2 = FilerFileField(blank=True)
        file3 = FilerFileField()
