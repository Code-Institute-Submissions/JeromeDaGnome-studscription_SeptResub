""" System Module """
from django.db import models
from django.contrib.auth.models import User
from products.models import Box

RATING = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)


class BoxReview(models.Model):
    """"
    Creates box review
    """
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    review_text = models.TextField()
    review_rating = models.IntegerField(choices=RATING, default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return box name rating on admin panel
        """
        return self.box.box_name
