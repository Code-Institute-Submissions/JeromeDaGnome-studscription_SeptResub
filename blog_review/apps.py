""" System Module """
from django.apps import AppConfig


class ProductReviewConfig(AppConfig):
    """
    Product review conf
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product_review'
