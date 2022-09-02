""" System Module """
from django import forms
from .models import CustomerReview


class AddReviewForm(forms.ModelForm):
    """
    Creates Add review form
    """
    class Meta:
        """
        Get model and add labels and widgets to the fields
        """
        model = CustomerReview
        fields = ('review_text', 'review_rating')
        labels = {
            "review_text": "Review",
            "review_rating": "Rating"
        }
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 3})
            }
