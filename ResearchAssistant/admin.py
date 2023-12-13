from django.contrib import admin
from .models import InputsForReportGeneration, ResearchHistory


@admin.register(InputsForReportGeneration)
class InputsForReportGenerationAdmin(admin.ModelAdmin):
    list_display = ('user', 'research_goal', 'research_objective', 'report_format')
    list_filter = ('report_format',)


@admin.register(ResearchHistory)
class ResearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'report_date_time', 'research_title')
    list_filter = ('user',)
    search_fields = ('user__username', 'research_title')


