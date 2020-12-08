from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(editable=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title
    def post_count(self):
        return self.posts.all().count()
class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def post_count(self):
        return self.posts.all().count()
class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    publishing_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True,null=True,upload_to='uploads/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(default="slug")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name="posts")
    tag = models.ManyToManyField(Tag, related_name="posts", blank=True)
    is_slider= models.BooleanField(default=False)
    hit = models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    def post_tags(self):
        return ','.join(str(tag) for tag in self.tag.all())

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    email = models.EmailField()
    name = models.CharField(max_length=20)
    content = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.post.title

