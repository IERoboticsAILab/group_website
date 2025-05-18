from django.shortcuts import render, get_object_or_404
from .models import (
    HomeContent, ResearchProject, TeamMember,
    Publication, LabInfo,
    BannerImage, ResearchLine
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
    research_lines = ResearchLine.objects.all()
    
    context = {
        'projects': all_projects,
        'research_lines': research_lines,
    }
    
    return render(request, 'core/projects.html', context)

def project_detail(request, slug):
    # Get the project
    project = get_object_or_404(ResearchProject, slug=slug)
    
    context = {
        'project': project,
    }
    
    return render(request, 'core/project_detail.html', context)

def research_line_detail(request, slug):
    # Get the research line
    research_line = get_object_or_404(ResearchLine, slug=slug)
    
    context = {
        'research_line': research_line,
    }
    
    return render(request, 'core/research_line_detail.html', context)

def contact(request):
    try:
        lab_info = LabInfo.objects.first()
    except LabInfo.DoesNotExist:
        lab_info = None
    
    context = {
        'lab_info': lab_info,
    }
    
    return render(request, 'core/contact.html', context)
