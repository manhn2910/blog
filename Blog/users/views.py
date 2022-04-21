from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from django.urls import reverse
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from core.models import Post
from users.models import Profile
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
# Create your views here.


@login_required
def dashboard(request):

    user = User.objects.get(username=request.user.username)
    form = ProfileForm(initial={'content': user.profile.description})

    data = {
        'user': user,
        'form': form,
    }

    return render(request, 'users/dashboard.html', data)


def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = get_object_or_404(user=request.user)
            profile.description = form.cleaned_data["content"]
            profile.save()
    return HttpResponseRedirect(reverse('dashboard'))


@login_required
def avatar_upload(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        image_src = fss.url(file)
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=user)
        profile.avatar = image_src
        profile.save()
        user.save()
        return redirect('users/dashboard.html')
    return render(request, 'users/avatar_upload.html')


@login_required
def my_post(request):
    user = request.user
    posts = Post.objects.all().filter(author=user)
    data = {
        'posts': posts
    }
    return render(request, 'users/my_post.html', data)


@login_required
def liked_post(request):
    user = request.user
    posts = Post.objects.filter(liked_by=user).order_by('-created_on')
    data = {
        'posts': posts
    }
    return render(request, 'users/liked_post.html', data)


def register(request):
    if request.method == 'GET':
        return render(request, 'users/register.html', {"form": CustomUserCreationForm})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.save()
            profile = Profile(user=user)
            profile.save()
            login(request, user)
            return redirect(reverse("dashboard"))
