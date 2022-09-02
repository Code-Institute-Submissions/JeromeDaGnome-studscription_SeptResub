""" System Module """
from django.db import models
from django.contrib.auth.models import User
from blogs.models import Blog

RATING = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)


class CustomerComment(models.Model):
    """"
    Creates blog review
    """
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    review_text = models.TextField()
    review_rating = models.IntegerField(choices=RATING, default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return blog name rating on admin panel
        """
        return self.blog.blog_name
