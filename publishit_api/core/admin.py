from django.contrib import admin

# Register your models here.
from .models import Article , Rating
admin.site.register(Rating)
admin.site.register(Article)