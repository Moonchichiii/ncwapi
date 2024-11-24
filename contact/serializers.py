from rest_framework import serializers
from .models import Contact
import re

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'message', 'created_at']

    def validate_email(self, value):
        # Example: Basic regex for email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value
