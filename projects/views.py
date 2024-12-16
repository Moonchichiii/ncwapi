from rest_framework import generics
from django_filters import rest_framework as filters
from .models import Project
from .serializers import ProjectSerializer

class ProjectFilter(filters.FilterSet):
    """
    Filter for Project model based on category, year, and featured fields.
    """
    category = filters.CharFilter(field_name='tags', method='filter_category')
    year = filters.CharFilter(lookup_expr='exact')

    def filter_category(self, queryset, name, value):
        return queryset.filter(tags__contains=[value])

    class Meta:
        model = Project
        fields = ['category', 'year', 'featured']

class ProjectListView(generics.ListAPIView):
    """
    API view to retrieve a list of projects with optional filtering.
    """
    serializer_class = ProjectSerializer
    filterset_class = ProjectFilter
    queryset = Project.objects.all()

    def get_queryset(self):
        queryset = Project.objects.all()
        if self.request.query_params.get('featured'):
            queryset = queryset.filter(featured=True)
        return queryset

class ProjectDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single project by ID.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer