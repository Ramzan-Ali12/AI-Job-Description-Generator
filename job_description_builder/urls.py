# job_description_builder/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView
from django.views.generic import TemplateView

urlpatterns = [
     # URL for generating the OpenAPI schema
   path('openapi/', SpectacularAPIView.as_view(), name='openapi-schema'),

    # URL for Swagger UI
    path(
        'docs/',
        TemplateView.as_view(
            template_name='swagger-ui.html',
            extra_context={'schema_url': 'openapi-schema'}
        ),
        name='swagger-ui'
    ),
    path("admin/", admin.site.urls),
    path('api/v1/', include('builder.urls')),

]


