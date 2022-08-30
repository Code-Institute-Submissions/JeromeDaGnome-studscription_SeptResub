from . import views
from django.urls import path


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/comment/',
         views.AddCommentView.as_view(), name='add_comment'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('characters/', views.CharacterList.as_view(), name='character_list'),
    path('character/<int:pk>/', views.CharacterDetail.as_view(),
         name='character_detail'),
    path('<pk>/update_character/',
         views.EditCharacterView.as_view(),
         name='update_character'
         ),
    path(
        '<pk>/delete_character/',
        views.DeleteCharacterView.as_view(),
        name='delete_character'
    ),
    path('characters/add/', views.AddCharactersView.as_view(),
         name="character_add"
         ),
]
