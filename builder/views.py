from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import JobDescriptionSerializer
from .utils import generate_job_description
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

import logging

# JWT api endpoints
@extend_schema(
    summary="Generate access and refresh tokens",
    description="Takes a set of user credentials and returns an access and refresh JSON web token pair.",
    tags=["jwt"],
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(
    summary="Refresh access token",
    description="Takes a valid refresh token and returns a new access token.",
    tags=["jwt"],
)
class CustomTokenRefreshView(TokenRefreshView):
    pass

@extend_schema(
    summary="Verify access token validity",
    description="Verifies if a given token is valid.",
    tags=["jwt"],
)
class CustomTokenVerifyView(TokenVerifyView):
    pass












# Set up logging
logger = logging.getLogger(__name__)


class JobDescriptionView(APIView):
    """
    API View to handle job description generation requests.
    """
    @extend_schema(
        request=JobDescriptionSerializer,
        responses={
          200: OpenApiResponse(response={"job_description": "string"}, description="Job description generated successfully."),
         400: OpenApiResponse(description="Bad Request due to invalid input."),
         500: OpenApiResponse(description="Internal Server Error encountered during processing.")
      },
        description="Handle POST request to create a job description based on company name and job title.",
        summary="Generate a job description",
        tags=["Job Description"],
    )
    def post(self, request):
        """
        Handle POST request to create a job description.

        Args:
            request (Request): The request object containing POST data.

        Returns:
            Response: A Response object containing the job description or validation errors.
        """
        serializer = JobDescriptionSerializer(data=request.data)

        if serializer.is_valid():
            # Extract validated data
            validated_data = serializer.validated_data
            job_title = validated_data.get('job_title')
            company_name = validated_data.get('company_name')
            company_overview = validated_data.get('company_overview', 'Default company overview')  
            role_overview = validated_data.get('role_overview', f"As a {job_title}, you will be responsible for...")
            key_responsibilities = validated_data.get('key_responsibilities', "● Design, code, and test software applications in Python...")
            qualifications = validated_data.get('qualifications', "● Bachelor's degree in Computer Science or a related field...")
            why_work_with_us = validated_data.get('why_work_with_us', "● Competitive salary package and benefits...")

            # Generate the job description
            try:
                job_description = generate_job_description(
                    job_title=job_title,
                    company_name=company_name,
                    company_overview=company_overview,
                    role_overview=role_overview,
                    key_responsibilities=key_responsibilities,
                    qualifications=qualifications,
                    why_work_with_us=why_work_with_us
                )
                return Response({"job_description": job_description}, status=status.HTTP_200_OK)

            except Exception as e:
                logger.error(f"Error generating job description: {e}")
                return Response({"error": "An error occurred while generating the job description."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return errors if the input data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
