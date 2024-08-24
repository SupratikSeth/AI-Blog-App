from django.urls import path
from . import views

app_name = 'blog_generator'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.user_signup, name='user_signup'),
    path('logout/', views.user_logout, name='user_logout'),
    path('generate-blog', views.generate_blog, name='generate_blog'),
    path('post-list/', views.post_list, name='post_list'),
    path('post-details/<int:id>', views.post_details, name="post_details"),
]
