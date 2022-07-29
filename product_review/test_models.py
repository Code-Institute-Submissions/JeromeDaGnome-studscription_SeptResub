""" System Module """
from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Box
from .models import BoxReview


class SetupModelTestCase(TestCase):
    """
    Base test case to be used in all models tests
    """
    def setUp(self):
        """ Setup for testing models """
        self.username = 'joe'
        self.password = '12345'
        self.user = User.objects.create_user(
            username=self.username,
            email='joe@doe.com',
            password=self.password)
        self.client.login(username='joe', password='12345')

        # Box creation
        self.box1 = Box.objects.create(
            box_name='testBox1',
            box_price=float('49.99'),
            category='Countries',
            box_description='test Box 1')
        self.review = BoxReview.objects.create(
            customer=self.user,
            box=self.box1,
            review_text="This is a review",
            review_rating="5",
            date_added="Oct. 24, 2021, 8:52 p.m.")


class BoxReviewTestCase(SetupModelTestCase):
    """
    Test BoxReview model function
    """
    def test__str__(self):
        """
        Test if order is returning correct string
        """
        self.assertEqual(str(self.review), 'testBox1')
