from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model."""
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'location', 
            'services', 'year', 'image', 'tags', 
            'link', 'external_link', 'featured'
        ]

    def to_representation(self, instance):
        """Convert tags from JSON string to list."""
        representation = super().to_representation(instance)
        if isinstance(representation['tags'], str):
            representation['tags'] = eval(representation['tags'])
        return representation