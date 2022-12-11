from django.contrib import admin

# Register your models here.
#after making models in model.py 
# we run makemigrations and then run migrate 
#still we have to connect /register to admin panel

from .models import Project, Review, Tag


admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)