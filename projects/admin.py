from django.contrib import admin
from django.utils.html import format_html
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'services', 'year', 'featured', 'display_tags', 'order')
    list_editable = ('order', 'featured')
    search_fields = ('title', 'description', 'location', 'services')
    list_filter = ('featured', 'year', 'services')
    readonly_fields = ('created_at',)
    ordering = ('order', '-created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'location', 'services', 'year')
        }),
        ('Media & Links', {
            'fields': ('image', 'link', 'external_link')
        }),
        ('Organization', {
            'fields': ('tags', 'featured', 'order')
        }),
        ('System Fields', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

    def display_tags(self, obj):
        if not obj.tags:
            return "-"
        tags_list = obj.tags if isinstance(obj.tags, list) else eval(obj.tags)
        return ", ".join(tags_list)
    display_tags.short_description = 'Tags'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['order'].help_text = 'Lower numbers appear first'
        form.base_fields['tags'].help_text = 'Enter tags as a Python list, e.g., ["Design", "Development"]'
        form.base_fields['link'].help_text = 'Internal path, e.g., /portfolio/project-name'
        return form

    class Media:
        css = {
            'all': ('admin/css/project_admin.css',)
        }
        js = ('admin/js/project_admin.js',)