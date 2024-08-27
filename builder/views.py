# generator/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import JobDescriptionSerializer
from .utils import generate_job_description
from django.http import HttpResponse


def home(request):
    if request.method == 'GET':
        return HttpResponse("Welcome to the Job Description Builder API!")
    else:
        return HttpResponseNotAllowed(['GET'])

class JobDescriptionView(APIView):
    
    @swagger_auto_schema(
        request_body=JobDescriptionSerializer,
        responses={200: 'Job description successfully generated.'}
    )
    def post(self, request):
        """Handle POST request to create a job description.

        Args:
            request (Request): The request object containing POST data.

        Returns:
            Response: A Response object containing the job description or validation errors.
        """
        serializer = JobDescriptionSerializer(data=request.data)
        
        # Validate the input data
        if serializer.is_valid():
            company_name = serializer.validated_data['company_name']
            job_title = serializer.validated_data['job_title']

            # Here, you would typically generate a job description using LangChain or another LLM
            # For now, let's assume you have a function `generate_job_description` that does this
            company_overview = "Provide a default company overview or fetch from a database"
            role_overview = f"As a {job_title}, you will be responsible for..."
            key_responsibilities = "● Design, code, and test software applications in Python..."
            qualifications = "● Bachelor's degree in Computer Science or a related field..."
            why_work_with_us = "● Competitive salary package and benefits..."

            # Call the function to generate the job description
            job_description = generate_job_description(
                job_title=job_title,
                company_name=company_name,
                company_overview=company_overview,
                role_overview=role_overview,
                key_responsibilities=key_responsibilities,
                qualifications=qualifications,
                why_work_with_us=why_work_with_us
            )

            # Return the generated job description in the response
            return Response({"job_description": job_description}, status=status.HTTP_200_OK)
        
        # Return errors if the input data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
