from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'location', 
            'services', 'year', 'image', 'tags', 
            'link', 'external_link', 'featured'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert tags from JSON to list.
        if isinstance(representation['tags'], str):
            representation['tags'] = eval(representation['tags'])
        return representation