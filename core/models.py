from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class BannerImage(models.Model):
    title = models.CharField(max_length=100, help_text="Image title for administrative purposes")
    image = models.ImageField(upload_to='banner/', help_text="Image will be resized to fit banner height")
    description = models.CharField(max_length=200, blank=True, help_text="Optional brief description of the image")
    order = models.PositiveIntegerField(default=0, help_text="Order in which the image will be displayed")
    active = models.BooleanField(default=True, help_text="Whether this image is displayed in the banner")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Banner Image"
        verbose_name_plural = "Banner Images"
    
    def __str__(self):
        return self.title

class HomeContent(models.Model):
    headline = models.CharField(max_length=200)
    subheadline = models.TextField()
    markdown_content = models.TextField(blank=True, help_text="Markdown content for the home page main section")
    youtube_video_url = models.URLField(blank=True, help_text="YouTube video embed URL for the home page")
    
    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Content"
    
    def __str__(self):
        return "Home Page Content"

class ResearchLine(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='research_lines/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Research Line"
        verbose_name_plural = "Research Lines"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('research_line_detail', kwargs={'slug': self.slug})

class ResearchProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    featured = models.BooleanField(default=False)
    research_line = models.ForeignKey(ResearchLine, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    content = models.TextField(blank=True, help_text="Detailed content for project detail page")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Research Project"
        verbose_name_plural = "Research Projects"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('PI', 'Principal Investigator'),
        ('POSTDOC', 'Postdoctoral Researcher'),
        ('PHD', 'PhD Student'),
        ('MS', 'Master Student'),
        ('UNDERGRAD', 'Undergraduate Student'),
        ('STAFF', 'Staff'),
        ('ALUMNI', 'Alumni'),
    ]
    
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    personal_website = models.URLField(blank=True)
    image = models.ImageField(upload_to='members/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
    
    def __str__(self):
        return self.name

class Publication(models.Model):
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=500)
    venue = models.CharField(max_length=200)
    year = models.CharField(max_length=4)
    doi = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True)
    abstract = models.TextField(blank=True)
    highlighted = models.BooleanField(default=False)
    authors_from_team = models.ManyToManyField(TeamMember, blank=True, related_name='publications')
    
    class Meta:
        ordering = ['-year', 'title']
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
    
    def __str__(self):
        return self.title

class AboutContent(models.Model):
    mission = models.TextField()
    history = models.TextField()
    
    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"
    
    def __str__(self):
        return "About Page Content"

class LabInfo(models.Model):
    department = models.CharField(max_length=200)
    building = models.CharField(max_length=200)
    room = models.CharField(max_length=50)
    institution = models.CharField(max_length=200)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    map_embed_url = models.URLField(help_text="Google Maps embed URL")
    
    class Meta:
        verbose_name = "Lab Information"
        verbose_name_plural = "Lab Information"
    
    def __str__(self):
        return f"Lab at {self.institution}"

class SocialMedia(models.Model):
    github = models.URLField(blank=True, help_text="GitHub repository URL")
    youtube = models.URLField(blank=True, help_text="YouTube channel URL")
    
    class Meta:
        verbose_name = "Social Media Links"
        verbose_name_plural = "Social Media Links"
    
    def __str__(self):
        return "Social Media Links"
    
    def has_any_links(self):
        return bool(self.github or self.youtube)
