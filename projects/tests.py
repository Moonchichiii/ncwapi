from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Project

# Create your tests here.


class ProjectAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.project = Project.objects.create(
            title='Test Project',
            description='A test project.',
            tags='test, django',
            featured=True
        )

    def test_get_project_list(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_project_detail(self):
        response = self.client.get(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Project')
