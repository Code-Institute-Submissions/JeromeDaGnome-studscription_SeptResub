from django.apps import AppConfig


class RatingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rating'

class Rating(models.Model):
    """
    Model to hold Customer Ratings for Products
    """
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)], null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} by {1}".format(self.rating, self.reviewer.username)
