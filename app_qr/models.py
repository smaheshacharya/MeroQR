from email.policy import default
from django.db import models
from django.forms import BooleanField
from django.db.models.signals import post_save
from django.dispatch import receiver

class Resturant(models.Model):
    user_id = models.OneToOneField('users.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100,blank=False,unique=True)
    sub_title = models.CharField(max_length=200)
    timing = models.CharField(max_length=100)    
    phone_number = models.CharField(max_length=10)
    description = models.TextField()
    logo = models.ImageField(upload_to='logo', blank=False, null=False)
    cover_image = models.ImageField(upload_to='cover_pic', blank=False, null=False)

    def __str__(self):
        return self.name

    object = models.Manager()
    REQUIRED_FIELDS = ['name','slug','sub_title','timing', 'phone_number','description','logo','cover_image']

class Category(models.Model):
    cat_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100,blank=False,unique=True)
    cat_image = models.ImageField(upload_to='cat_pic', blank=False, null=False)
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)


    def __str__(self):
        return self.cat_name

    object = models.Manager()
    REQUIRED_FIELDS = ['cat_name','slug','cat_image','resturant']


class Product(models.Model):
    category_id = models.ForeignKey(Category, blank=False, null=False, default="", related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    pro_pic = models.ImageField(upload_to='pro_pic', blank=False, null=False)
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)

    
    def __str__(self):
        return self.name

    object = models.Manager()
    REQUIRED_FIELDS = ['name','price','pro_pic', 'category_id','resturant']



class Qr(models.Model):
    link = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    qr_image = models.ImageField(upload_to='qr_image', blank=False, null=False)
    resturant = models.OneToOneField(Resturant, on_delete=models.CASCADE)

    
    def __str__(self):
        return str(self.resturant)

    object = models.Manager()
    REQUIRED_FIELDS = ['link','slug','qr_image','resturant']


@receiver(post_save, sender=Resturant)
def create_qr(sender, instance, created, **kwargs):
    if created:
        Qr.object.create(resturant=instance)


@receiver(post_save, sender=Resturant)
def update_qr(sender, instance, created, **kwargs):
    if created == False:
        instance.qr.save()
        