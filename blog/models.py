from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        if not self.title:
            return ""
        else:
            return self.title  # noqa

    def number_of_likes(self):
        if not self.likes:
            return 0
        else:
            return self.likes.count()  # noqa


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return '%s -%s' % (self.post, self.name)


class Characters(models.Model):
    name = models.CharField(max_length=200)
    image = CloudinaryField('image', default='placeholder')
    bio = models.TextField()
    tag_lines = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        if not self.name:
            return ""
        else:
            return self.name  # noqa
