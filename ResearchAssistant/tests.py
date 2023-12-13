from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import InputsForReportGeneration, ResearchHistory

User = get_user_model()

class TestInputsForReportGeneration(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.input_report = InputsForReportGeneration.objects.create(
            user=self.user,
            research_goal='Test research goal',
            research_objective='Test research objective',
            research_parameters='Test research parameters',
            report_format='xlsx',  # Choose the format for testing
        )

    def test_inputs_for_report_creation(self):
        self.assertEqual(self.input_report.user.username, 'testuser')
        self.assertEqual(self.input_report.research_goal, 'Test research goal')
        self.assertEqual(self.input_report.research_objective, 'Test research objective')
        self.assertEqual(self.input_report.research_parameters, 'Test research parameters')
        self.assertEqual(self.input_report.report_format, 'xlsx')

    def test_uploaded_file(self):
        # Assuming file is uploaded
        self.input_report.uploaded_file = 'path_to_test_file'  # Set the file path
        self.input_report.save()
        self.assertIsNotNone(self.input_report.uploaded_file)

class TestResearchHistory(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.research_history = ResearchHistory.objects.create(
            user=self.user,
            research_title='Test Research',
            sources='Test sources',
        )

    def test_research_history_creation(self):
        self.assertEqual(self.research_history.user.username, 'testuser')
        self.assertEqual(self.research_history.research_title, 'Test Research')
        self.assertEqual(self.research_history.sources, 'Test sources')
        self.assertIsNotNone(self.research_history.report_date_time)

    def test_generate_report_filename(self):
        filename = 'test_report.docx'  # Replace with the desired filename
        generated_filename = self.research_history.generate_report_filename(filename)
        expected_filename = f'{self.user.username}_Test Research_{filename}'
        self.assertEqual(generated_filename, expected_filename)
