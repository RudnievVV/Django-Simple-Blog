from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Post
from .forms import PostForm, CommentForm
from .services import PostClass, CommentClass
import copy


def home_page(request):
    posts = PostClass(request).get_all_posts()

    return render(request, 'blog/home.html', {'posts': posts})


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = PostClass(request).post_create(form)

            return redirect('post-detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_create.html', {'form': form})


def post_detail(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    comments_sort_options = copy.deepcopy(settings.COMMENTS_SORT_OPTIONS)
    sorting_symbols = copy.deepcopy(settings.SORTING_SYMBOLS)

    context = PostClass(request).post_detail(post, sorting_symbols, comments_sort_options)

    return render(request, 'blog/post_detail.html', context)


def comment_create(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            PostClass(request).post_comment_create(post, form)

            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/comment_create.html', {'form': form})


def comment_to_comment_create(request, pk, comm, comm_sub):
    post = get_object_or_404(Post, pk=pk)
    user, comment_title = CommentClass.user_and_title_defining(pk, comm, comm_sub)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            PostClass(request).post_comment_to_comment_create(pk, post, form, comm, comm_sub)

            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/comment_to_comment.html', {'form': form, 'user': user, 'comment_title': comment_title})
