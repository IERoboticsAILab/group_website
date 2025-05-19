from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from filer.fields.image import FilerImageField

class HomeContent(models.Model):
    headline = models.CharField(max_length=200)
    subheadline = models.CharField(max_length=200)
    about_markdown_content = models.TextField(blank=True, help_text="Markdown content for the home page main section")
    youtube_video_url = models.URLField(blank=True, help_text="YouTube video embed URL for the home page")
    section_markdown_content = models.TextField(blank=True, help_text="Markdown content for the second home page section")
    section_image = FilerImageField(null=True, blank=True, related_name="home_section_images", on_delete=models.SET_NULL, help_text="Image for the second home page section")
    
    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Content"
    
    def __str__(self):
        return "Home Page Content"

class ResearchLine(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    video_url = models.URLField(blank=True, help_text="YouTube video embed URL for the research line")
    banner_image = FilerImageField(null=True, blank=True, related_name="research_line_banners", on_delete=models.SET_NULL, help_text="Banner image for the research line")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    team_members = models.ManyToManyField('TeamMember', blank=True, related_name='research_lines')
    publications = models.ManyToManyField('Publication', blank=True, related_name='research_lines')
    projects = models.ManyToManyField('ResearchProject', blank=True, related_name='research_lines_set')
    
    class Meta:
        ordering = ['-date']
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

class ResearchLineGalleryImage(models.Model):
    research_line = models.ForeignKey(ResearchLine, on_delete=models.CASCADE, related_name='gallery_images')
    image = FilerImageField(null=True, blank=True, related_name="research_line_gallery", on_delete=models.SET_NULL)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        
    def __str__(self):
        return f"Image for {self.research_line.title}"

class ResearchProject(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    video_url = models.URLField(blank=True, help_text="YouTube video embed URL for the project")
    banner_image = FilerImageField(null=True, blank=True, related_name="project_banners", on_delete=models.SET_NULL, help_text="Banner image for the project")
    team_members = models.ManyToManyField('TeamMember', blank=True, related_name='projects')
    publications = models.ManyToManyField('Publication', blank=True, related_name='projects')
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    content = models.TextField(blank=True, help_text="Detailed content for project detail page")
    
    class Meta:
        ordering = ['-date']
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

class ProjectGalleryImage(models.Model):
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name='gallery_images')
    image = FilerImageField(null=True, blank=True, related_name="project_gallery", on_delete=models.SET_NULL)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Project Gallery Image"
        verbose_name_plural = "Project Gallery Images"
        
    def __str__(self):
        return f"Image for {self.project.title}"

class TeamMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    personal_website = models.URLField(blank=True)
    image = FilerImageField(null=True, blank=True, related_name="member_images", on_delete=models.SET_NULL)
    principal_investigator = models.BooleanField(default=False)
    alum = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['last_name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Publication(models.Model):
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=500)
    paperlink = models.URLField(blank=True)
    pdflink = models.URLField(blank=True)
    abstract = models.TextField(blank=True)
    date = models.DateField(blank=True, null=True)
    image = FilerImageField(null=True, blank=True, related_name="publication_images", on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ['-date', 'title']
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
    
    def __str__(self):
        return self.title

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

class JobPosition(models.Model):
    title = models.CharField(max_length=200)
    position = models.CharField(max_length=200, help_text="Position title/type")
    contact_email = models.EmailField(help_text="Contact email for applications")
    date_posted = models.DateField(auto_now_add=True)
    application_deadline = models.DateField(help_text="Application deadline")
    description = models.TextField(help_text="Detailed description of the position")
    requirements = models.TextField(help_text="Requirements for the position")
    instructions = models.TextField(help_text="Application instructions", blank=True)
    notes = models.TextField(blank=True, help_text="Additional notes about the position")
    is_active = models.BooleanField(default=True, help_text="Whether this position is currently open")
    
    class Meta:
        ordering = ['-date_posted']
        verbose_name = "Job Position"
        verbose_name_plural = "Job Positions"
    
    def __str__(self):
        return self.title
