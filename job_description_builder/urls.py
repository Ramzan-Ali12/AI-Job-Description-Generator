# job_description_builder/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
     # URL for generating the OpenAPI schema
   path('openapi/', SpectacularAPIView.as_view(), name='openapi-schema'),

    # URL for Swagger UI
    path('docs/v1/', SpectacularAPIView.as_view(), name='openapi-schema') ,
    path('docs/', SpectacularSwaggerView.as_view(url_name='openapi-schema'), name='docs-ui'),    
    path("admin/", admin.site.urls),
    path('api/v1/', include('builder.urls')),
    path('api/v1/', include('subscriptions.urls')),
]


