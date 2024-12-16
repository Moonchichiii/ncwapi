from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/contact/', include('contact.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/chatbot/', include('chatbot.urls')),
]

"""
URL configuration for the backend application.
Includes routes for admin, contact, projects, and chatbot APIs.
"""