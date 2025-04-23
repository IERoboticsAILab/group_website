from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def research(request):
    # Example research projects
    research_projects = [
        {
            'title': 'Project 1',
            'description': 'Description of research project 1',
            'image': 'images/project1.jpg',
        },
        {
            'title': 'Project 2',
            'description': 'Description of research project 2',
            'image': 'images/project2.jpg',
        },
        {
            'title': 'Project 3',
            'description': 'Description of research project 3',
            'image': 'images/project3.jpg',
        },
    ]
    return render(request, 'core/research.html', {'research_projects': research_projects})

def members(request):
    # Example team members
    team_members = [
        {
            'name': 'Prof. John Doe',
            'title': 'Principal Investigator',
            'bio': 'Short biography of Prof. John Doe',
            'image': 'images/member1.jpg',
            'email': 'john.doe@example.com',
        },
        {
            'name': 'Dr. Jane Smith',
            'title': 'Postdoctoral Researcher',
            'bio': 'Short biography of Dr. Jane Smith',
            'image': 'images/member2.jpg',
            'email': 'jane.smith@example.com',
        },
        {
            'name': 'Alex Johnson',
            'title': 'PhD Student',
            'bio': 'Short biography of Alex Johnson',
            'image': 'images/member3.jpg',
            'email': 'alex.johnson@example.com',
        },
    ]
    return render(request, 'core/members.html', {'team_members': team_members})

def publications(request):
    # Example publications
    publications_list = [
        {
            'title': 'Example Publication Title 1',
            'authors': 'Doe, J., Smith, J., Johnson, A.',
            'venue': 'Journal of Example Research, 2023',
            'doi': '10.1234/example.123456',
            'link': 'https://example.com/publication1',
            'year': '2023',
        },
        {
            'title': 'Example Publication Title 2',
            'authors': 'Smith, J., Doe, J., Johnson, A.',
            'venue': 'Conference on Example Topics, 2022',
            'doi': '10.1234/example.654321',
            'link': 'https://example.com/publication2',
            'year': '2022',
        },
        {
            'title': 'Example Publication Title 3',
            'authors': 'Johnson, A., Doe, J., Smith, J.',
            'venue': 'International Journal of Examples, 2021',
            'doi': '10.1234/example.789012',
            'link': 'https://example.com/publication3',
            'year': '2021',
        },
    ]
    return render(request, 'core/publications.html', {'publications': publications_list})

def contact(request):
    return render(request, 'core/contact.html')
