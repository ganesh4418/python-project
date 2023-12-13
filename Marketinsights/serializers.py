from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomizeInsights


class CustomizeInsightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomizeInsights
        fields = '__all__'

    def validate(self, data):
        finance = data.get('finance', False)
        healthcare = data.get('healthcare', False)
        technology = data.get('technology', False)
        refresh_frequency = data.get('refresh_frequency')

        # Check if at least one industry is chosen
        if not any([finance, healthcare, technology]):
            raise ValidationError("At least one industry must be selected")

        # Check if refresh_frequency is either 'daily', 'weekly', or 'monthly'

        request = self.context.get('request')
        if request and request.method == 'PATCH':
            # If it's a PUT request, allow any value for refresh_frequency
            return data

        # For other methods like POST, enforce specific refresh_frequency values
        valid_frequencies = ['daily', 'weekly', 'biweekly', 'monthly']
        if refresh_frequency not in valid_frequencies:
            raise serializers.ValidationError(
                "Select refresh frequency from given options"
            )
        return data

