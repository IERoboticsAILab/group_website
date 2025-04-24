from django.contrib import admin
from django.utils.html import format_html
from .models import (
    HomeContent, ResearchArea, ResearchProject, TeamMember, 
    Publication, LabInfo,
    BannerImage
)

# Content Management
@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    app_label = 'Content Management'
    def has_add_permission(self, request):
        # Only allow one instance of HomeContent
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
@admin.register(LabInfo)
class LabInfoAdmin(admin.ModelAdmin):
    app_label = 'Content Management'
    def has_add_permission(self, request):
        # Only allow one instance of LabInfo
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

# Research
@admin.register(ResearchArea)
class ResearchAreaAdmin(admin.ModelAdmin):
    app_label = 'Research'
    list_display = ('name', 'order')
    list_editable = ('order',)

@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    app_label = 'Research'
    list_display = ('title', 'research_area', 'featured', 'order')
    list_filter = ('research_area', 'featured')
    list_editable = ('featured', 'order')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description', 'content')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'image', 'research_area')
        }),
        ('Display Options', {
            'fields': ('featured', 'order')
        }),
        ('Detailed Content', {
            'fields': ('content',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    app_label = 'Research'
    list_display = ('title', 'venue', 'year', 'highlighted')
    list_filter = ('year', 'highlighted')
    list_editable = ('highlighted',)
    search_fields = ('title', 'authors', 'abstract')
    filter_horizontal = ('authors_from_team',)

# Team
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    app_label = 'Team'
    list_display = ('name', 'title', 'role', 'email', 'active', 'order')
    list_filter = ('role', 'active')
    list_editable = ('active', 'order')
    search_fields = ('name', 'email', 'bio')


# Media & Display
@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    app_label = 'Media & Display'
    list_display = ('title', 'image_preview', 'order', 'active')
    list_editable = ('order', 'active')
    search_fields = ('title', 'description')
    list_filter = ('active',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "No Image"
    
    image_preview.short_description = 'Preview'

