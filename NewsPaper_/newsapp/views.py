from datetime import datetime

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Post, Category, User
from .filters import NewsFilter
from .forms import NewsForm, UserForm
from django.urls import reverse_lazy

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic.edit import CreateView

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

class CategoryList(ListView):

    model = Category
    ordering = 'name'
    template_name = 'category.html'
    context_object_name = 'category'
    paginate_by = 10
    # permission_required = ('newsapp.view_category')

@login_required
def add_subscribe(request, pk):
    subscriber = request.user
    subscriber.save()
    category = Category.objects.get(id=pk)
    category.subscribers.add(subscriber)

    return redirect('/news/')

class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-dateCreation'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'newsid.html'
    context_object_name = 'post'

class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'
    permission_required = ('newsapp.add_post')

    def form_valid(self, form):
        posttype = form.save(commit=False)
        posttype.categoryType = 'NW'
        return super().form_valid(form)

class NewsEdit(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('newsapp.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = '/news/'

class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'article_create.html'
    permission_required = ('newsapp.add_post')

    def form_valid(self, form):
        posttype = form.save(commit=False)
        posttype.categoryType = 'AR'
        return super().form_valid(form)

class ArticleEdit(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'article_edit.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('newsapp.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')

class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'user_update.html'
    form_class = UserForm
    success_url = reverse_lazy('news_list')

    def get_object(self, **kwargs):
        return self.request.user

from django.http import HttpResponse
from django.views import View
from .tasks import weekly_send_for_subscribers
# notify_new_post hello, printer

class IndexView(View):
    def get(self, request):
        # notify_new_post.delay()
        weekly_send_for_subscribers.delay()
        return HttpResponse('Hello!')










