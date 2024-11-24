from django.contrib import admin
from .models import Project


# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured')
    search_fields = ('title', 'tags')
    list_filter = ('featured',)
    readonly_fields = ('created_at',)
