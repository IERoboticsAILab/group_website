from django.contrib import admin
from .models import (
    HomeContent, ResearchArea, ResearchProject, TeamMember, 
    Publication, AboutContent, LabInfo, FundingSource, Collaborator
)

@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance of HomeContent
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(ResearchArea)
class ResearchAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)

@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'research_area', 'featured', 'order')
    list_filter = ('research_area', 'featured')
    list_editable = ('featured', 'order')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'role', 'email', 'active', 'order')
    list_filter = ('role', 'active')
    list_editable = ('active', 'order')
    search_fields = ('name', 'email', 'bio')

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'venue', 'year', 'highlighted')
    list_filter = ('year', 'highlighted')
    list_editable = ('highlighted',)
    search_fields = ('title', 'authors', 'abstract')
    filter_horizontal = ('authors_from_team',)

@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance of AboutContent
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(LabInfo)
class LabInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance of LabInfo
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(FundingSource)
class FundingSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')

@admin.register(Collaborator)
class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ('institution', 'website')
