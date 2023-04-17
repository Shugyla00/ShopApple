from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=250)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=150)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class Item(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    memory = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    money = models.PositiveIntegerField(default=0)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=150)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item_show', kwargs={'cat_slug': self.category.slug, 'slug': self.slug})


class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(default=1)
    isOrdered = models.BooleanField(default=False)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pk


