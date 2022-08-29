from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from product_review.forms import AddReviewForm
from product_review.models import CustomerReview
from .models import Product, Category
from .forms import ProductForm


# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
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
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST" and request.user.is_authenticated:
        review_rating = request.POST.get('review_rating', 5)
        review_text = request.POST.get('review_text', '')

        review = CustomerReview.objects.create(
            product=product,
            customer=request.user,
            review_rating=review_rating,
            review_text=review_text
            )
        messages.success(request, "Your review was successfully added!")
        return redirect(reverse('product_detail', args=[product.id]))

    review_form = AddReviewForm
    reviews = CustomerReview.objects.filter(product=product.id).order_by('-date_added')[:2]
    context = {
        'product': product,
        'review_form':review_form,
        'reviews':reviews,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def edit_review(request, pk):
    """
    Edit reviews
    """
    review = get_object_or_404(CustomerReview, pk=pk)
    if request.user == review.customer:
        if request.method == 'POST':
            form = AddReviewForm(request.POST, request.FILES, instance=review)
            rating = request.POST.get('review_rating')
            form.fields['review_rating'].choices = [(int(rating), int(rating))]
            if form.is_valid():
                form.save()

                review = get_object_or_404(CustomerReview, pk=pk)
                context = {
                    'review': review,
                }
                return redirect(reverse('product_detail', args=[review.product.pk]))
            else:
                messages.error(request, 'Failed to edit your product.\
                    Please, ensure your form is valid')
        else:
            form = AddReviewForm(instance=review)

        context = {
            'form': form,
            'review': review,
        }
        return render(request, 'product_review/edit_review.html', context)
    else:
        messages.info(request, 'Sorry, you cannot change this review.')
        return redirect(reverse('product_detail', args=[review.product.pk]))


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


@login_required
def delete_review(request, pk):
    """
    Delete review
    """
    review = get_object_or_404(BoxReview, pk=pk)
    if request.user == review.customer:
        try:
            review = get_object_or_404(BoxReview, pk=pk)
            review.delete()
            messages.success(request, 'Your review was deleted')
            return redirect(reverse('box_details', args=[review.box.pk]))
        except:
            messages.error(request, 'Something went wrong.\
                Your review was not deleted .')
    else:
        messages.error(request, 'Sorry, you do not have permittion \
            to access this page')
        return redirect(reverse('box_details', args=[review.box.pk]))
