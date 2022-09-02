""" System Module """
from django.apps import AppConfig


class BlogReviewConfig(AppConfig):
    """
    Blog review conf
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_review'
