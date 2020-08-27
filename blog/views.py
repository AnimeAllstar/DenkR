from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

def home(request):
    context = {
        "posts": Post.objects.all()
    }
    return render(request, "blog/home.html", context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 15


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False




def about(request):
    return render(request, "blog/about.html", {"title": "DenkR - About"})


def connections(request):
    return render(request, "blog/connections.html", {"title": "Your Connections"})


def top(request):
    return render(request, "blog/top.html", {"title": "DenkR - Top Posts"})


def forum(request):
    return render(request, "blog/forum.html", {"title": "DenkR - Investor Forum"})

def likeView(request,pk):
    temp = 0
    if 'unlike_id' in request.POST:
        temp = request.POST.get('unlike_id')
        post = get_object_or_404(Post,id=temp)
        post.likes.remove(request.user)
    elif 'like_id' in request.POST:
        temp = request.POST.get('like_id')
        post = get_object_or_404(Post,id=temp)
        post.likes.add(request.user)
    return HttpResponseRedirect("/#" + temp)        
