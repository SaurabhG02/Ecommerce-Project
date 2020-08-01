import random
import os
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save , post_save
from .utils import unqiue_slug_generator
from django.urls import reverse, reverse_lazy
# Create your models here.
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name , ext= os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    print(instance)
    print(filename)
    new_filename = random.randint(1,3184654)
    name , ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename,final_filename=final_filename)

class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)

    def search(self, query):
        lookups = Q(title__icontains=query) | Q(description__icontains=query)
        return self.filter(lookups).distinct()
    




class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def features(self):
        return self.get_queryset().filter()

    def get_by_id(self,id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        lookups = (Q(title__icontains=query) | 
                  Q(description__icontains=query) |
                  Q(price__icontains=query))
        return self.filter(lookups).distinct()

class Product(models.Model):
    title       = models.CharField(max_length=100)
    slug        = models.SlugField(default='Prod', blank=True, unique=True)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2,max_digits=8)
    image       = models.ImageField(upload_to='products/', null=True, blank=True)
    featured    = models.BooleanField(default=False)


    objects = ProductManager()

    def get_absolute_url(self):
        # return "product/{slug}/".format(slug=self.slug)
        return reverse('product-detail', kwargs={'slug':self.slug})

    def __str__(self):
        return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unqiue_slug_generator(instance)
    
pre_save.connect(product_pre_save_receiver, sender=Product)