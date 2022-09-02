""" System Module """
from django.urls import path
from products import views

urlpatterns = [
    path("edit_review/<int:pk>/", views.edit_review, name="edit_review"),
    path("delete_review/<int:pk>/", views.delete_review, name="delete_review"),
]
