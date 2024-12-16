from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Project

class ProjectAPITest(TestCase):
    """Test suite for the Project API."""

    def setUp(self):
        """Set up the test client and create a test project."""
        self.client = APIClient()
        self.project = Project.objects.create(
            title='Test Project',
            description='A test project.',
            tags='test, django',
            featured=True
        )

    def test_get_project_list(self):
        """Test retrieving the list of projects."""
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_project_detail(self):
        """Test retrieving a single project's details."""
        response = self.client.get(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Project')
