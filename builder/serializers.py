# generator/serializers.py
from rest_framework import serializers

class JobDescriptionSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255)
    job_title = serializers.CharField(max_length=255)
