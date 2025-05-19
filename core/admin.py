from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import redirect
from .models import (
    HomeContent, ResearchProject, TeamMember, 
    Publication, LabInfo,
    ResearchLine, SocialMedia,
    ResearchLineGalleryImage, ProjectGalleryImage,
    JobPosition
)

# Content Management
@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    app_label = 'Content Management'
    fields = ('headline', 'subheadline', 'about_markdown_content', 'youtube_video_url', 'section_markdown_content', 'section_image')
    
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def changelist_view(self, request, extra_context=None):
        if self.model.objects.exists():
            obj = self.model.objects.first()
            return redirect('admin:core_homecontent_change', obj.id)
        return super().changelist_view(request, extra_context)

@admin.register(LabInfo)
class LabInfoAdmin(admin.ModelAdmin):
    app_label = 'Content Management'
    
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def changelist_view(self, request, extra_context=None):
        if self.model.objects.exists():
            obj = self.model.objects.first()
            return redirect('admin:core_labinfo_change', obj.id)
        return super().changelist_view(request, extra_context)

# Research

class ResearchLineGalleryImageInline(admin.TabularInline):
    model = ResearchLineGalleryImage
    extra = 1
    fields = ('image', 'caption', 'order')

class ProjectGalleryImageInline(admin.TabularInline):
    model = ProjectGalleryImage
    extra = 1
    fields = ('image', 'caption', 'order')

@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    app_label = 'Research'
    list_display = ('title', 'date')
    list_filter = ()
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description', 'content')
    filter_horizontal = ('team_members', 'publications')
    inlines = [ProjectGalleryImageInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'banner_image', 'video_url')
        }),
        ('Related Content', {
            'fields': ('team_members', 'publications')
        }),
        ('Detailed Content', {
            'fields': ('content',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    app_label = 'Research'
    list_display = ('title', 'date')
    list_filter = ('date',)
    search_fields = ('title', 'authors', 'abstract')

# Team
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    app_label = 'Team'
    list_display = ('first_name', 'last_name', 'email')
    list_filter = ()
    search_fields = ('first_name', 'last_name', 'email')


# Media & Display
@admin.register(ResearchLine)
class ResearchLineAdmin(admin.ModelAdmin):
    app_label = 'Research'
    list_display = ('title', 'date')
    list_filter = ()
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
    filter_horizontal = ('team_members', 'publications', 'projects')
    inlines = [ResearchLineGalleryImageInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'banner_image', 'video_url')
        }),
        ('Related Content', {
            'fields': ('team_members', 'publications', 'projects')
        }),
    )

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    app_label = 'Content Management'
    list_display = ('github', 'youtube')
    
    def has_add_permission(self, request):
        # Only allow one instance of SocialMedia
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def changelist_view(self, request, extra_context=None):
        # If a SocialMedia instance exists, redirect to its change page
        if self.model.objects.exists():
            obj = self.model.objects.first()
            return redirect('admin:core_socialmedia_change', obj.id)
        return super().changelist_view(request, extra_context)

@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'contact_email', 'application_deadline')
    list_filter = ()
    search_fields = ('title', 'description')

