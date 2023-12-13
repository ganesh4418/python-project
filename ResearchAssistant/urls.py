from django.urls import path
from . import views
from .views import ResearchHistoryDownloadView
from .views import get_trending_headlines_view
from .views import InputsForReportGenerationList, InputsForReportGenerationDetail
from .views import RecentResearchTitlesView

urlpatterns = [
    path('inputs-report-generation/', InputsForReportGenerationList.as_view(), name='report-generation-list'),
    path('inputs-report-generation/<int:pk>/', InputsForReportGenerationDetail.as_view(), name='report-generation-detail'),
    path('research-history/', views.ResearchHistoryList.as_view(), name='researchhistory-list'),
    path('recent-research-titles/', RecentResearchTitlesView.as_view(), name='recent_research_titles_for_user'),
    path('download_report/<str:research_title>/', ResearchHistoryDownloadView.as_view(), name='research-history-download'),
    path('trending-headlines/', get_trending_headlines_view, name='get_trending_headlines'),
]