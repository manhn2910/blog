from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_listing, name='post_listing'),
    path('categories/', views.category_listing, name='category_listing'),
    path('categories/<category_id>/',
         views.category_view, name='category_view'),
    path('post/<int:pk>/', views.post_view, name='post_view'),
    path('user_info/', views.request_user_info),
    path('member_place/', views.member_place),
    path('staff_place/', views.staff_place),
    path('add_messages/', views.add_messages),
    path('like/<int:pk>/', views.like_post, name='like_post')
]
