""" System Module """
from django.contrib import admin
from .models import CustomerComment


class CustomerCommentAdmin(admin.ModelAdmin):
    """
    Create Order option on admin
    """
    list_display = [
        'customer',
        'date_added',
        'review_text',
        'review_rating',
    ]


admin.site.register(CustomerComment, CustomerCommentAdmin)
