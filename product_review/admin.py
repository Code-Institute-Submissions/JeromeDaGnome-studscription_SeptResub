""" System Module """
from django.contrib import admin
from .models import BoxReview


class BoxReviewAdmin(admin.ModelAdmin):
    """
    Create Order option on admin
    """
    list_display = [
        'customer',
        'date_added',
        'box',
        'review_text',
        'review_rating',
    ]


admin.site.register(BoxReview, BoxReviewAdmin)
