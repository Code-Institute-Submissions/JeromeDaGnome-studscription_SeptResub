from . import views
from django.urls import path


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/comment/',
         views.AddCommentView.as_view(), name='add_comment'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]
