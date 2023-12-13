from django.contrib import admin
from .models import CustomizeInsights

from django.contrib import admin
from .models import CustomizeInsights

@admin.register(CustomizeInsights)
class CustomizeInsightsAdmin(admin.ModelAdmin):
    list_display = ('user', 'finance', 'healthcare', 'technology', 'refresh_frequency')
    list_filter = ('refresh_frequency',)
    search_fields = ('user__username',)

#admin.site.register(CustomizeInsights, CustomizeInsightsAdmin)