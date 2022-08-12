from email.policy import default
from django.db import models
from django.forms import BooleanField


class Category(models.Model):
    cat_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100,blank=False,unique=True)
    cat_description = models.TextField()
    cat_image = models.ImageField(upload_to='cat_pic', blank=False, null=False)
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.cat_name

    object = models.Manager()
    REQUIRED_FIELDS = ['cat_name','slug','cat_description','cat_image']


class Product(models.Model):
    category_id = models.ForeignKey(Category, blank=False, null=False, default="", related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    pro_description = models.TextField()
    today_special = BooleanField()
    pro_pic = models.ImageField(upload_to='pro_pic', blank=False, null=False)
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    object = models.Manager()
    REQUIRED_FIELDS = ['name','price','pro_description','pro_pic', 'category_id', 'today_special']

