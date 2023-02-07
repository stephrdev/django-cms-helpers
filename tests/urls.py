from django.contrib import admin
from django.urls import include, re_path
from django.views.generic import TemplateView


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^non-cms/', TemplateView.as_view(template_name='empty_template.html')),
    re_path(r'', include('cms.urls')),
]
