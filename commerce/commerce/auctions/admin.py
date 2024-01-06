from django.contrib import admin
from .models import User, Items, Comment, Bid
# Register your models here.

admin.site.register(User)
admin.site.register(Items)
admin.site.register(Comment)
admin.site.register(Bid)