from django.contrib import admin
from .models import Post, Comment, Characters
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on', 'title')
    search_fileds = ['title', 'content']
    summernote_fields = ('content')


@admin.register(Comment)
@admin.register(Characters)
class CharacterAdmin(admin.ModelAdmin):
    list_filter = ()
