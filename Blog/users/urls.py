from django.urls import include, re_path, path
from users import views as user_views

urlpatterns = [
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^dashboard/avatar_upload',
            user_views.avatar_upload, name='avatar_upload'),
    re_path(r'^dashboard', user_views.dashboard, name='dashboard'),
    re_path(r'^oauth/', include('social_django.urls')),
    re_path(r'^register/', user_views.register, name='register'),
    re_path(r'^my_post/', user_views.my_post, name='my_post'),
    re_path(r'^liked_post/', user_views.liked_post, name='liked_post'),
]
