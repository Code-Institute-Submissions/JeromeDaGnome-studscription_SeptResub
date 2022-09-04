""" System Module """
from django import forms
from .models import CustomerComment


class AddReviewForm(forms.ModelForm):
    """
    Creates Add review form
    """
    class Meta:
        """
        Get model and add labels and widgets to the fields
        """
        model = CustomerComment
        fields = ('review_text',)
        labels = {
            "review_text": "Comment",
        }
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 3})
            }
