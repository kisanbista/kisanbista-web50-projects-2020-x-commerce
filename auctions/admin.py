from django.contrib import admin
from .models import Product,Watchlist,Bid,User,Comment
# Register your models here.
admin.site.register(Product)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(Comment)