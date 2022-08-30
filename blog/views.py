from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views import generic, View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # noqa
from .models import Post, Comment, Characters
from .forms import CommentForm, CharacterEditForm, CharacterAddForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog_details.html'


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "blog_details.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
        messages.success = "Comment added!"


class CharacterList(ListView):
    model = Characters
    queryset = Characters.objects.order_by("name")
    template_name = "character_list.html"


class CharacterDetail(DetailView):
    model = Characters
    template_name = "character_detail.html"


@method_decorator(login_required(
    login_url='/accounts/login/'), name='dispatch')
class EditCharacterView(UpdateView):
    model = Characters
    form_class = CharacterEditForm
    template_name = 'edit_character.html'

    def form_valid(self, form):
        """
        Upon success prompt the user with a success message.
        """
        messages.success(self.request, "Edit made!")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        return reverse_lazy("character_detail", args=[str(self.object.pk)])


@method_decorator(login_required(
    login_url='/accounts/login/'), name='dispatch')
class DeleteCharacterView(DeleteView):
    model = Characters
    template_name = 'delete_character.html'
    messages_success = 'Character deleted!'

    def get_success_url(self, **kwargs):
        return reverse_lazy("character_list")

    def delete(self, request, *args, **kwargs):
        """
        Success message to be displayed after deletion of post.
        Help from multiple stackoverflow posts.
        """
        messages.success(self.request, self.messages_success)
        return super(DeleteCharacterView, self).delete(request, *args, **kwargs)  # noqa


@method_decorator(login_required(
    login_url='/accounts/login/'), name='dispatch')
class AddCharactersView(CreateView):
    model = Characters
    form_class = CharacterAddForm
    template_name = 'add_characters.html'

    def form_valid(self, form):
        """
        Upon success prompt the user with a success message.
        """
        messages.success(self.request, "Character made!")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        return reverse_lazy("character_detail", args=[str(self.object.pk)])


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)

        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('blog_detail', args=[slug]))
