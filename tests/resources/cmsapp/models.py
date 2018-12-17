from cms.extensions import TitleExtension
from cms.extensions.extension_pool import extension_pool

from cms_helpers.filer_fields import FilerFileField
from django.db import models


@extension_pool.register
class ExtensionModel(TitleExtension):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Extension'

    def __str__(self):
        return self.name


class FileModel(models.Model):
        file1 = FilerFileField(null=True)
        file2 = FilerFileField(blank=True)
        file3 = FilerFileField()
