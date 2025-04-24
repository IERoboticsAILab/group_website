from django.shortcuts import render, get_object_or_404
from .models import (
    HomeContent, ResearchArea, ResearchProject, TeamMember,
    Publication, AboutContent, LabInfo, FundingSource, Collaborator,
    BannerImage
)

# Create your views here.

def home(request):
    # Get home content or use a default
    try:
        home_content = HomeContent.objects.first()
    except HomeContent.DoesNotExist:
        home_content = None
    
    # Get featured research projects
    featured_projects = ResearchProject.objects.filter(featured=True)[:3]
    
    # Get active team members
    team_members = TeamMember.objects.filter(active=True)[:3]
    
    # Get highlighted publications
    highlighted_pubs = Publication.objects.filter(highlighted=True)[:3]
    
    # Get active banner images
    banner_images = BannerImage.objects.filter(active=True)
    
    context = {
        'home_content': home_content,
        'featured_projects': featured_projects,
        'featured_members': team_members,
        'highlighted_publications': highlighted_pubs,
        'banner_images': banner_images,
    }
    
    return render(request, 'core/home.html', context)

def about(request):
    # Get about content or use a default
    try:
        about_content = AboutContent.objects.first()
    except AboutContent.DoesNotExist:
        about_content = None
    
    # Get lab info
    try:
        lab_info = LabInfo.objects.first()
    except LabInfo.DoesNotExist:
        lab_info = None
    
    # Get funding sources
    funding_sources = FundingSource.objects.all()
    
    context = {
        'about_content': about_content,
        'lab_info': lab_info,
        'funding_sources': funding_sources,
    }
    
    return render(request, 'core/about.html', context)

def research(request):
    # Get all research areas with their projects
    research_areas = ResearchArea.objects.all()
    
    # Get all research projects
    research_projects = ResearchProject.objects.all()
    
    # Get collaborators
    collaborators = Collaborator.objects.all()
    
    context = {
        'research_areas': research_areas,
        'research_projects': research_projects,
        'collaborators': collaborators,
    }
    
    return render(request, 'core/research.html', context)

def people(request):
    # Get active team members by role
    pis = TeamMember.objects.filter(active=True, role='PI')
    postdocs = TeamMember.objects.filter(active=True, role='POSTDOC')
    phd_students = TeamMember.objects.filter(active=True, role='PHD')
    masters = TeamMember.objects.filter(active=True, role='MS')
    undergrads = TeamMember.objects.filter(active=True, role='UNDERGRAD')
    staff = TeamMember.objects.filter(active=True, role='STAFF')
    
    # Alumni
    alumni = TeamMember.objects.filter(active=False) | TeamMember.objects.filter(role='ALUMNI')
    
    context = {
        'pis': pis,
        'postdocs': postdocs,
        'phd_students': phd_students,
        'masters': masters,
        'undergrads': undergrads,
        'staff': staff,
        'alumni': alumni,
    }
    
    return render(request, 'core/people.html', context)

def publications(request):
    # Get all publications ordered by year
    all_publications = Publication.objects.all()
    
    # Get unique years for filter
    publication_years = Publication.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    context = {
        'publications': all_publications,
        'publication_years': publication_years,
    }
    
    return render(request, 'core/publications.html', context)

def projects(request):
    # Get all projects
    all_projects = ResearchProject.objects.all()
    
    # Get research areas for filtering
    research_areas = ResearchArea.objects.all()
    
    context = {
        'projects': all_projects,
        'research_areas': research_areas,
    }
    
    return render(request, 'core/projects.html', context)

def project_detail(request, slug):
    # Get the project
    project = get_object_or_404(ResearchProject, slug=slug)
    
    # Get related projects from the same research area
    if project.research_area:
        related_projects = ResearchProject.objects.filter(
            research_area=project.research_area
        ).exclude(id=project.id)[:3]
    else:
        related_projects = ResearchProject.objects.exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    
    return render(request, 'core/project_detail.html', context)

def contact(request):
    # Get lab info for contact details
    try:
        lab_info = LabInfo.objects.first()
    except LabInfo.DoesNotExist:
        lab_info = None
    
    context = {
        'lab_info': lab_info,
    }
    
    return render(request, 'core/contact.html', context)
