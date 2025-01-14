from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from users.forms import UserRegisterForm
from .models import Post, Friend, Ideathon
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
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
import pytz


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    order_by = ['-date']
    paginate_by = 15


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        if self.request.user.is_anonymous:
            context = super(UserPostListView, self).get_context_data(**kwargs)
            return context
        else:
            context = super(UserPostListView, self).get_context_data(**kwargs)
            friend, created = Friend.objects.get_or_create(
                current_user=self.request.user)
            friends = friend.users.all()
            context.update({
                'friends': friends,
                'current_user': self.request.user
            })
            return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')


class PostDetailView(LoginRequiredMixin, DetailView):
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


@login_required
def connections(request):
    friend, created = Friend.objects.get_or_create(current_user=request.user)
    friends = friend.users.all()
    context = {
        'friends': friends
    }
    return render(request, "blog/connections.html", context)


@login_required
def uni_resources(request):
    return render(request, "blog/uni_resources.html", {"title": "DenkR - University Resources"})


@login_required
def forum(request):
    return render(request, "blog/forum.html", {"title": "DenkR - Investor Forum"})


@login_required
def ideathon(request):
    ideathons = Ideathon.objects.all()
    myIdeathons = []
    pastIdeathons = []
    for x in ideathons:
        if request.user in x.participants.all():
            myIdeathons.append(x)
            utc = pytz.UTC
            if datetime.now().replace(tzinfo=utc) > x.Date.replace(tzinfo=utc):
                pastIdeathons.append(x)
    context = {
        'myIdeathons': list(set(myIdeathons)),
        'pastIdeathons': list(set(pastIdeathons)),
        'currentIdeathon': ideathons.first()
    }
    return render(request, "blog/ideathon.html", context)


def likeView(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        liked_post = get_object_or_404(Post, pk=post_id)
        if request.user in liked_post.likes.all():
            liked_post.likes.remove(request.user)
        else:
            liked_post.likes.add(request.user)
        return HttpResponse("Success!")
    else:
        return HttpResponse("Request method is not a GET")


@login_required
def add_friend(request, username):
    main_user = request.user
    to_connect = User.objects.get(username=username)

    # check if users are already connected
    friends = Friend.objects.filter(current_user=main_user, users=to_connect)
    is_connected = True if friends else False

    if is_connected:
        Friend.remove_friend(current_user=main_user, new_friend=to_connect)
        is_connected = False
    else:
        Friend.make_friend(current_user=main_user, new_friend=to_connect)
        is_connected = True

    return redirect('/user/' + username)


def searchView(request):
    if request.method == 'GET':
        search_value = request.GET.get('value')
        if len(search_value.strip()) == 0:
            return HttpResponseRedirect("/")
        else:
            search_field = str(request.GET.get('search_option'))
            queryset = []
            if search_field != "User":
                for i in search_value.split(" "):
                    lower_i = i.lower()
                    for j in Post.objects.all():
                        lower_titles = [x.lower() for x in j.title.split(" ")]
                        if lower_i in lower_titles:
                            queryset.append(j)
            else:
                for k in Post.objects.all():
                    if search_value.lower() in k.author.username.lower():
                        queryset.append(k)
            return render(request, 'blog/search.html', {'posts': list(set(queryset))})


def registerView(request):
    if request.method == 'GET':
        current = Ideathon.objects.first()
        if not request.user in current.participants.all():
            current.participants.add(request.user)
            return HttpResponse("User Added")
        else:
            return HttpResponse("User Already Present")
    else:
        return HttpResponse("Request method is not a GET")
