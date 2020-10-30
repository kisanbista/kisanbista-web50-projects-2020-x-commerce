from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
CATEGORY = (
    ('kids','KIDS'),
    ('women', 'WOMEN'),
    ('electronics','ELECTRONICS'),
    ('groceries','GROCERIES'),
    ('other','OTHER'),
)
class Product(models.Model):
    product_name = models.CharField(max_length = 64)
    product_description = models.TextField(blank = True)
    product_price = models.DecimalField(max_digits = 100, decimal_places = 2)
    product_url = models.CharField(max_length = 256, blank = True)
    product_created = models.DateField(auto_now_add = True)
    category = models.CharField(max_length=14, choices=CATEGORY, default='other')
    dateCompleted = models.DateField(blank = True, null = True)
	# user = models.ForeignKey(User,on_delete = models.CASCADE)
    user = models.ForeignKey(User,on_delete = models.CASCADE)

    def __str__(self):
        return self.product_name

class Watchlist(models.Model):   
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField(null = True,blank = True)

    def __str__(self):
        return self.user.username

class Bid(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    bidding_price = models.DecimalField(max_digits = 100, decimal_places = 2)

    def __str__(self):
        return self.user.username