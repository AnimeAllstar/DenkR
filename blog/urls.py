from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    likeView,
    searchView,
)


urlpatterns = [
    path("", PostListView.as_view(), name="blog-home"),
    path("user/<str:username>", UserPostListView.as_view(), name="user-posts"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("about/", views.about, name="blog-about"),
    path("connect/add/<str:username>>", views.add_friend, name="add-friend"),

    path("connections/", views.connections, name="blog-connections"),
    path("university-resources/", views.uni_resources, name="blog-uni-resources"),
    path("investor-forum/", views.forum, name="blog-forum"),
    path("ideathon/", views.ideathon, name="ideathon"),
    
    path('like/',likeView, name='like-post'),
    path('search/',searchView, name='search-post')
]
