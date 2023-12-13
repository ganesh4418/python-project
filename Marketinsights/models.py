from django.db import models
from django.conf import settings


class CustomizeInsights(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    finance = models.BooleanField(default=False, blank=False)
    healthcare = models.BooleanField(default=False, blank=True)
    technology = models.BooleanField(default=False, blank=True)
    refresh_frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('biweekly', 'Biweekly'),
            ('monthly', 'Monthly'),
        ],
        default=None,
        null=True,
        blank=True
    )