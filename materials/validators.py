from rest_framework.exceptions import ValidationError

def validate_youtube_url(value):
    """Разрешены только ссылки на youtube.com"""
    if "youtube.com" not in value and "youtu.be" not in value:
        raise ValidationError("Разрешены только ссылки на YouTube.")
    return value