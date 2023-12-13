from django.http import JsonResponse, FileResponse
from rest_framework import generics, status
from rest_framework.response import Response
from . import generate_report
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import ResearchHistory, InputsForReportGeneration
from .serializers import ResearchHistorySerializer, InputsForReportGenerationSerializer
from rest_framework.parsers import MultiPartParser
from .trending_headlines import get_trending_headlines
import json
from os.path import splitext
from rest_framework.views import APIView


class InputsForReportGenerationList(generics.CreateAPIView):
    queryset = InputsForReportGeneration.objects.all()
    serializer_class = InputsForReportGenerationSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the data to the database
            serializer.save()
            # Call the research_report_generation function
            report_result, sources = generate_report.research_report_generation(request)
            response_data = {
                'report_result': report_result,
                'sources': sources
            }
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InputsForReportGenerationDetail(generics.RetrieveUpdateAPIView):
    queryset = InputsForReportGeneration.objects.all()
    serializer_class = InputsForReportGenerationSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Call the research_report_generation function
            report_result, sources = generate_report.research_report_generation(request)
            response_data = {
                'report_result': report_result,
                'sources': sources
            }
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Call the research_report_generation function
            report_result, sources = generate_report.research_report_generation(request)
            response_data = {
                'report_result': report_result,
                'sources': sources
            }
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResearchHistoryList(generics.ListCreateAPIView):
    queryset = ResearchHistory.objects.all()
    serializer_class = ResearchHistorySerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResearchHistoryDownloadView(generics.RetrieveAPIView):
    queryset = ResearchHistory.objects.all()
    serializer_class = ResearchHistorySerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [AllowAny]
    lookup_field = 'research_title'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file_path = instance.generated_report.path
        response = FileResponse(open(file_path, 'rb'))

        # Set the Content-Disposition header for attachment
        response['Content-Disposition'] = f'attachment; filename="{instance.generated_report.name}"'

        return response


class RecentResearchTitlesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = recent_research_titles_for_user(request)
        return JsonResponse(data, safe=False)

def recent_research_titles_for_user(request):
    user_id = request.user.id

    # Query the ResearchHistory model to get the 10 most recent research titles for the specific user
    recent_research = ResearchHistory.objects.filter(
        user_id=user_id
    ).order_by('-report_date_time')[:10].values('research_title', 'generated_report')

    # Convert the queryset to a list of dictionaries
    recent_titles = list(recent_research)

    # Convert generated_report values to strings
    for title_info in recent_titles:
        title_info['generated_report'] = str(title_info['generated_report'])

        _, file_extension = splitext(title_info['generated_report'])
        title_info['file_format'] = file_extension

    # Return the data in JSON format
    research_data = {'recent_titles': recent_titles}
    return research_data


def get_trending_headlines_view(request):
    try:
        trending_headlines_json = get_trending_headlines()
        trending_headlines_data = json.loads(trending_headlines_json)  # Convert the JSON string to a Python object
        return JsonResponse({"trending_headlines": trending_headlines_data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)