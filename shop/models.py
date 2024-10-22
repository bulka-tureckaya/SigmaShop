from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)

    name = models.CharField(max_length=150, db_index=True, verbose_name='Name')
    slug = models.CharField(max_length=150, db_index=True, unique=True, default=uuid.uuid4, verbose_name='Link')
    image = models.ImageField(upload_to=' shop/static/shop/img/product/%Y/%m/%d', blank=True)
    description = models.TextField(max_length=1000, blank=True, verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price', default=0.00)
    
    available = models.BooleanField(default=True, verbose_name='Availability')
    created = models.DateTimeField(default=timezone.now, verbose_name='Uploaded')
    uploaded = models.DateTimeField(auto_now=True, verbose_name='Edited')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        index_together = (('id', 'slug'), )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

