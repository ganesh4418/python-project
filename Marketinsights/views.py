from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CustomizeInsights
from .serializers import CustomizeInsightsSerializer
from .Intellisense_Market_Insights import get_market_insights
from rest_framework.response import Response
import json
from django.http import JsonResponse, FileResponse


class CustomizeInsightsList(generics.ListCreateAPIView):
    queryset = CustomizeInsights.objects.all()
    serializer_class = CustomizeInsightsSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomizeInsightsDetail(generics.RetrieveUpdateAPIView):
    queryset = CustomizeInsights.objects.all()
    serializer_class = CustomizeInsightsSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            # Get the initial data before saving
            initial_data = serializer.to_representation(instance)

            serializer.save()

            # Get the updated data after saving
            updated_instance = CustomizeInsights.objects.get(pk=instance.pk)
            updated_serializer = self.get_serializer(updated_instance)
            updated_data = updated_serializer.data

            # Compare initial data and updated data to find modified fields
            modified_fields = {
                key: updated_data[key] for key, value in initial_data.items()
                if updated_data.get(key) != value
            }

            return Response(modified_fields)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_market_insights_view(request):
    try:
        market_insights_json = get_market_insights()
        market_insights_data = json.loads(market_insights_json)  # Convert the JSON string to a Python object
        return JsonResponse({"market_insights": market_insights_data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)