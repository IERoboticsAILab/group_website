from .models import SocialMedia

def social_media_links(request):
    try:
        social_media = SocialMedia.objects.first()
    except SocialMedia.DoesNotExist:
        social_media = None
    return {'social_media': social_media} 