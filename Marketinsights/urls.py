from django.urls import path
from . import views
from .views import get_market_insights_view

urlpatterns = [
    path('customize_insights/', views.CustomizeInsightsList.as_view(), name='customize_insights-list'),
    path('customize_insights/<int:pk>/', views.CustomizeInsightsDetail.as_view(), name='customize_insights-detail'),
    path('market_insights/', get_market_insights_view, name='get_trending_headlines'),
]