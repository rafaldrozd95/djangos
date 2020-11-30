from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
# Create your views here.
from .models import Post, Category, Tag
from .forms import PostCreationForm, PostUpdateForm
from django.template.defaultfilters import slugify



class IndexView(ListView):
    template_name = 'posts/index.html'
    model = Post
    context_object_name = 'posts'
    def get_context_data(self, **kwargs):
        slider_posts = Post.objects.all().filter(is_slider=True)
        context = super().get_context_data(**kwargs)
        context['sliders'] = slider_posts
        return context

class PostDetail(DetailView):
    template_name='posts/detail.html'
    model = Post
    context_object_name = 'single'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CategoryDetail(ListView):
    template_name='categories/category_detail.html'
    model = Post
    context_object_name = 'posts'
    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Post.objects.filter(category=self.category).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['category'] = self.category
        return context


class TagDetail(ListView):
    template_name = 'tags/tag_detail.html'
    model = Post
    context_object_name = 'posts'
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        return Post.objects.filter(tag=self.tag).order_by('-id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        context['tag'] = self.tag
        return context

class CreatePostView(CreateView):
    template_name = 'posts/create-post.html'
    form_class = PostCreationForm
    model = Post
    def get_success_url(self):
        return reverse('detail', kwargs={
            'pk': self.object.pk,
            'slug': self.object.slug
        })
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()

        tags = self.request.POST.get("tag").split(',')
        for tag in tags:
            current_tag = Tag.objects.all().filter(slug=slugify(tag))
            if current_tag.count() < 1:
                created_tag = Tag.objects.create(title=tag)
                form.instance.tag.add(created_tag)
            else:
                existing_tag = Tag.objects.get(slug=slugify(tag))
                form.instance.tag.add(existing_tag)

        return super().form_valid(form)

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'posts/update-post.html'
    form_class = PostUpdateForm
    def get_success_url(self):
        return reverse('detail', kwargs={
            'pk': self.object.pk,
            'slug': self.object.slug
        })