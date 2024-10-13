# generator/urls.py
from django.urls import path
from .views import JobDescriptionView , CustomTokenObtainPairView,CustomTokenRefreshView,CustomTokenVerifyView

urlpatterns = [
    path('generate-job-description/', JobDescriptionView.as_view(), name='generate_job_description'),
        # Auth-related JWT Endpoints (auth operations)
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/jwt/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/jwt/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
]
