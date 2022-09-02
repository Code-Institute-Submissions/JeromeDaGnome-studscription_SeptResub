""" System Module """
from django.contrib import admin
from .models import CustomerReview


class CustomerReviewAdmin(admin.ModelAdmin):
    """
    Create Order option on admin
    """
    list_display = [
        'customer',
        'date_added',
        'product',
        'review_text',
        'review_rating',
    ]


admin.site.register(CustomerReview, CustomerReviewAdmin)
