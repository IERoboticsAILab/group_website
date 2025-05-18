from django.shortcuts import render, get_object_or_404
from .models import (
    HomeContent, ResearchProject, TeamMember,
    Publication, LabInfo, ResearchLine
)

# Create your views here.

def home(request):
    # Get home content or use a default
    try:
        home_content = HomeContent.objects.first()
    except HomeContent.DoesNotExist:
        home_content = None
    
    context = {
        'home_content': home_content,
        'about_markdown_content': home_content.about_markdown_content if home_content else '',
        'section_markdown_content': home_content.section_markdown_content if home_content else '',
        'youtube_video_url': home_content.youtube_video_url if home_content else '',
        'section_image': home_content.section_image if home_content else '',
    }
    
    return render(request, 'core/home.html', context)


def people(request):
    # Get active team members by role
    pis = TeamMember.objects.filter(principal_investigator=True)
    people = TeamMember.objects.filter(principal_investigator=False)
    alumni = TeamMember.objects.filter(alum=True)
    
    context = {
        'pis': pis,
        'people': people,
        'alumni': alumni,
    }
    
    return render(request, 'core/people.html', context)

def publications(request):
    # Get all publications ordered by date
    all_publications = Publication.objects.all().order_by('-date')
    
    # Get unique years for filter
    publication_years = Publication.objects.dates('date', 'year', order='DESC')
    
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
