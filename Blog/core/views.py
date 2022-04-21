from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Category, Post, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
# Create your views here.


def category_listing(request):
    categories = Category.objects.all()
    data = {
        'categories': categories,
    }
    return render(request, 'blog/category.html', data)


def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(categories__id__contains=category_id
                                ).order_by('-created_on')
    data = {
        'category': category,
        "posts": posts,
    }
    print(data)
    return render(request, 'blog/category_view.html', data)


def post_listing(request):
    posts = Post.objects.all().order_by('-created_on')
    print(posts)
    data = {
        'posts': posts,
    }

    return render(request, 'blog/index.html', data)


def post_view(request, pk):
    post = Post.objects.get(pk=pk)

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                user=form.cleaned_data["author"],
                content=form.cleaned_data["body"],
                post=post
            )
            comment.save()

    comments = Comment.objects.filter(post=post)
    data = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, 'blog/post_view.html', data)


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if not request.user in post.liked_by.all():
        post.liked_by.add(request.user)
    else:
        post.liked_by.remove(request.user)
    return HttpResponseRedirect(reverse('post_view', args=[str(pk)]))


def request_user_info(request):
    text = f"""
        Selected HttpRequest.user attributes:

        username:     {request.user.username}
        is_anonymous: {request.user.is_anonymous}
        is_staff:     {request.user.is_staff}
        is_superuser: {request.user.is_superuser}
        is_active:    {request.user.is_active}
    """

    return HttpResponse(text, content_type='text/plain')


@ login_required
def member_place(request):
    return HttpResponse('Area of members!', content_type='text/plain')


@ login_required
def add_messages(request):
    username = request.user.username
    messages.add_message(request, messages.INFO, f"Hello { username }")
    messages.add_message(request, messages.WARNING, "WARNING!!")
    return HttpResponse('Message added', content_type='text/plain')


@ user_passes_test(lambda user: user.is_staff)
def staff_place(request):
    return HttpResponse('Area of Staff!', content_type='text/plain')
