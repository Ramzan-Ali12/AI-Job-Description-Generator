# generator/urls.py
from django.urls import path
from .views import JobDescriptionView

urlpatterns = [
    path('generate-job-description/', JobDescriptionView.as_view(), name='generate_job_description'),
]
