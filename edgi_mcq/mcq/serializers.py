from django.contrib.auth import authenticate
from rest_framework import serializers

from mcq.models import AddQuestion, ApplicantMCQTest


class AddQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddQuestion
        fields = '__all__'


class ApplicantMCQTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantMCQTest
        fields = '__all__'




