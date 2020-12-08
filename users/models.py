from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from PIL import Image
from django.db.models.signals import post_save
# Create your models here.
class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True)
    birth_date = models.DateField(null=True)
    image = models.ImageField(blank=True,null=True,upload_to='users/', default='users/annonymous.png')
    slug = models.SlugField(editable=False)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfileModel, self).save(*args, **kwargs)
        img = Image.open(self.image.path)  
        print(img)
        if img.width > 200 or img.height > 200:
            print('here ia m')
            img.thumbnail((200,200))
            img.save(self.image.path)
        return 
        
    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfileModel.objects.create(user = instance)
    return

post_save.connect(create_profile, sender=User)