from blog.forms import CommentForm, PostForm
from blog.mixins import CommentUpdateDeleteMixin, PostUpdateDeleteMixin
from blog.models import Category, Post
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)

User = get_user_model()


class PostListView(ListView):
    paginate_by = 10
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.published.all()


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostDetailView(DetailView):
    model = Post
    form_class = CommentForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['comments'] = self.object.comments.all()
        return context

    def get_object(self, queryset=None):
        post = super().get_object()
        if post.author == self.request.user:
            return post
        if post.is_published:
            return post
        raise Http404


class PostUpdateView(PostUpdateDeleteMixin, UpdateView):

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(PostUpdateDeleteMixin, DeleteView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class ProfileView(ListView):
    paginate_by = 10
    template_name = 'blog/profile.html'

    def get_queryset(self):
        username = self.kwargs.get('username')
        if self.request.user.username == username:
            return (
                Post.objects.filter(author__username=username)
                .annotate(comment_count=Count('comments'))
                .order_by('-pub_date')
            )
        return Post.published.filter(author__username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentUpdateView(CommentUpdateDeleteMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentUpdateDeleteMixin, DeleteView):
    pass


class CategoryListView(ListView):
    paginate_by = 10
    template_name = 'blog/category.html'

    def get_queryset(self):
        return Post.published.filter(
            category__slug=self.kwargs['category_slug']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category.objects.filter(is_published=True),
            slug=self.kwargs['category_slug']
        )
        return context
