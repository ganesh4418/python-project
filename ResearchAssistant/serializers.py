from rest_framework import serializers
from .models import InputsForReportGeneration, ResearchHistory


class InputsForReportGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputsForReportGeneration
        fields = '__all__'


class ResearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchHistory
        fields = '__all__'
