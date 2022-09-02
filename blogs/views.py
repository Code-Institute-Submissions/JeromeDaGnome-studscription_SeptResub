from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from blog_review.forms import AddReviewForm
from blog_review.models import CustomerComment
from .models import Blog
from .forms import BlogForm


# Create your views here.


def all_blogs(request):
    """ A view to show all blogs, including sorting and search queries """

    blogs = Blog.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                blogs = blogs.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            blogs = blogs.order_by(sortkey)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('blogs'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            blogs = blogs.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'blogs': blogs,
        'search_term': query,
        'current_sorting': current_sorting,
    }

    return render(request, 'blogs/blogs.html', context)


def blog_detail(request, blog_id):
    """ A view to show individual blog details """

    blog = get_object_or_404(Blog, pk=blog_id)

    if request.method == "POST" and request.user.is_authenticated:
        review_rating = request.POST.get('review_rating', 5)
        review_text = request.POST.get('review_text', '')

        review = CustomerComment.objects.create(
            blog=blog,
            customer=request.user,
            review_rating=review_rating,
            review_text=review_text
        )
        messages.success(request, "Your review was successfully added!")
        return redirect(reverse('blog_detail', args=[blog.id]))

    review_form = AddReviewForm
    reviews = CustomerComment.objects.filter(
        blog=blog.id).order_by('-date_added')[:2]
    context = {
        'blog': blog,
        'review_form': review_form,
        'reviews': reviews,
    }

    return render(request, 'blogs/blog_detail.html', context)


@login_required
def edit_review(request, pk):
    """
    Edit reviews
    """
    review = get_object_or_404(CustomerComment, pk=pk)
    if request.user == review.customer:
        if request.method == 'POST':
            form = AddReviewForm(request.POST, request.FILES, instance=review)
            rating = request.POST.get('review_rating')
            form.fields['review_rating'].choices = [(int(rating), int(rating))]
            if form.is_valid():
                form.save()

                review = get_object_or_404(CustomerComment, pk=pk)
                context = {
                    'review': review,
                }
                return redirect(reverse('blog_detail', args=[review.blog.pk]))
            else:
                messages.error(request, 'Failed to edit your blog.\
                    Please, ensure your form is valid')
        else:
            form = AddReviewForm(instance=review)

        context = {
            'form': form,
            'review': review,
        }
        return render(request, 'blog_review/edit_review.html', context)
    else:
        messages.info(request, 'Sorry, you cannot change this review.')
        return redirect(reverse('blog_detail', args=[review.blog.pk]))


@login_required
def add_blog(request):
    """ Add a blog to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save()
            messages.success(request, 'Successfully added blog!')
            return redirect(reverse('blog_detail', args=[blog.id]))
        else:
            messages.error(
                request, 'Failed to add blog. Please ensure the form is valid.')
    else:
        form = BlogForm()

    template = 'blogs/add_blog.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_blog(request, blog_id):
    """ Edit a blog in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated blog!')
            return redirect(reverse('blog_detail', args=[blog.id]))
        else:
            messages.error(
                request, 'Failed to update blog. Please ensure the form is valid.')
    else:
        form = BlogForm(instance=blog)
        messages.info(request, f'You are editing {blog.name}')

    template = 'blogs/edit_blog.html'
    context = {
        'form': form,
        'blog': blog,
    }

    return render(request, template, context)


@login_required
def delete_blog(request, blog_id):
    """ Delete a blog from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    messages.success(request, 'Blog deleted!')
    return redirect(reverse('blogs'))


@login_required
def delete_review(request, pk):
    """
    Delete review
    """
    review = get_object_or_404(CustomerComment, pk=pk)
    if request.user == review.customer:
        try:
            review = get_object_or_404(CustomerComment, pk=pk)
            review.delete()
            messages.success(request, 'Your review was deleted')
            return redirect(reverse('blog_detail', args=[review.blog.pk]))
        except:
            messages.error(request, 'Something went wrong.\
                Your review was not deleted .')
    else:
        messages.error(request, 'Sorry, you do not have permition \
            to access this page')
        return redirect(reverse('blog_detail', args=[review.blog.pk]))
