from rest_framework import generics
from .models import Contact
from .serializers import ContactSerializer
from .tasks import send_contact_email
import logging
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

# Create your views here.

class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    @method_decorator(ratelimit(key='ip', rate='5/m', block=True)) 
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        contact = serializer.save()
        try:
            send_contact_email.delay(contact.name, contact.email, contact.message)
        except Exception as e:
            logger.error(f"Error queuing email task: {e}")
            contact.delete()
            raise
