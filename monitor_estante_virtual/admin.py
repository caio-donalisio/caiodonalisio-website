from django.contrib import admin

from .models import Query, Collection, Book

admin.site.register(Query)
admin.site.register(Collection)
admin.site.register(Book)