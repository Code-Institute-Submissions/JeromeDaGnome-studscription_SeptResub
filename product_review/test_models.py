""" System Module """
from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product
from .models import ProductReview


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
        self.product1 = Product.objects.create(
            product_name='testproduct1',
            product_price=float('49.99'),
            category='Countries',
            box_description='test Box 1')
        self.review = ProductReview.objects.create(
            customer=self.user,
            product=self.product1,
            review_text="This is a review",
            review_rating="5",
            date_added="Oct. 24, 2021, 8:52 p.m.")


class ProductReviewTestCase(SetupModelTestCase):
    """
    Test ProductReview model function
    """
    def test__str__(self):
        """
        Test if order is returning correct string
        """
        self.assertEqual(str(self.review), 'testProduct1')
