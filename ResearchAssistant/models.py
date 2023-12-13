from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_word_count(value):
    words = value.split()
    if len(words) > 500:
        raise ValidationError('Maximum words limit is 500.')


class InputsForReportGeneration(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    research_goal = models.TextField(validators=[validate_word_count])
    research_objective = models.TextField(validators=[validate_word_count])
    research_parameters = models.TextField(validators=[validate_word_count])
    additional_text_input = models.TextField(default=None,null=True, blank=True)

    # Define choices for the file format
    REPORT_FORMAT_CHOICES = [
        ('xlsx', 'Excel'),
        ('pptx', 'Powerpoint'),
        ('docx', 'Doc'),
        ('pdf', 'PDF'),
    ]

    report_format = models.CharField(max_length=10, choices=REPORT_FORMAT_CHOICES)
    uploaded_file = models.FileField(upload_to='input_files/', null=True, blank=True)


class ResearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    report_date_time = models.DateTimeField(auto_now_add=True)
    research_title = models.CharField(max_length=200, unique=True)
    sources = models.TextField()


    def generate_report_filename(self, filename):
        return f'{self.user.username}_{self.research_title}_{filename}'

    generated_report = models.FileField(upload_to='reports_generated/')

