from rest_framework import serializers
from django.core.validators import EmailValidator
import re
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[EmailValidator()])

    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'message', 'created_at']

    