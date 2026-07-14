from cms.extensions import PageContentExtensionAdmin
from django.contrib import admin

from .models import ExtensionModel


admin.site.register(ExtensionModel, PageContentExtensionAdmin)
