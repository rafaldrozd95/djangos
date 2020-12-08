from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.db.models import F, Q
# Create your views here.
from .models import Post, Category, Tag, Comment
from .forms import PostCreationForm, PostUpdateForm, CreateCommentForm
from django.template.defaultfilters import slugify



class IndexView(ListView):
    template_name = 'posts/index.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    def get_context_data(self, **kwargs):
        slider_posts = Post.objects.all().filter(is_slider=True)
        context = super().get_context_data(**kwargs)
        context['sliders'] = slider_posts
        return context

class PostDetail(DetailView, FormMixin):
    template_name='posts/detail.html'
    model = Post
    context_object_name = 'single'
    form_class = CreateCommentForm
    def get_success_url(self):
        return redirect(reverse('detail', kwargs={"pk": self.kwargs.pk, "slug": self.kwargs.slug}))
    def get(self,request, *args, **kwargs):
        self.hit = Post.objects.filter(id=self.kwargs['pk']).update(hit=F('hit')+1)
        return super().get(request, *args, **kwargs)
    def form_valid(self,form):
        self.object = self.get_object()
        form.instance.post = self.object
        if form.is_valid():
            form.save()
            return super(PostDetail, self).form_valid(form)
        else: 
            return super(PostDetail,self).form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_comments = Comment.objects.filter(post__id__exact = self.object.id)
        context['next'] = Post.objects.all().filter(id__exact=(self.kwargs['pk']+1)).first()
        context['prev'] = Post.objects.all().filter(id__exact=(self.kwargs['pk']-1)).first()
        context['form'] = self.get_form()
        context['comments'] = related_comments
        return context
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        return self.form_valid(form)


class CategoryDetail(ListView):
    template_name='categories/category_detail.html'
    model = Post
    context_object_name = 'posts'
    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Post.objects.filter(category=self.category).order_by('-publishing_date')

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
    def get(self, request, **kwargs):
            self.object = self.get_object()
            if self.object.user != request.user:
                return redirect('/')
            return super().get(request,**kwargs)    

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.tag.clear()   
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

class DeletePostView(DeleteView):
        model = Post
        success_url = '/'
        template_name = 'posts/delete.html'
        context_object_name = 'post'

        def delete(self, request, *args, **kwargs):
            self.object = self.get_object()
            if self.object.user == request.user:
                self.object.delete()
            else:
                return redirect(self.success_url)
        def get(self, request, *args, **kwargs):
            self.object = self.get_object()
            if self.object.user != request.user:
                return redirect('/')

class SearchView(ListView):
    template_name = 'posts/search.html'
    model = Post
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Post.objects.filter(Q(title__icontains=query)|
            Q(content__icontains=query)|Q(tag__title__icontains=query)).order_by('id').distinct()
        return Post.objects.all().order_by('id')