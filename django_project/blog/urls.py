from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('post/create/', views.post_create, name='post-create'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/comment/', views.comment_create, name='comment-create'),
    path('post/<int:pk>/<int:comm>/<int:comm_sub>/', views.comment_to_comment_create, name='comment-to-comment-create'),
]