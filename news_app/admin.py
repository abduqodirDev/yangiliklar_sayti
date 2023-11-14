from django.contrib import admin
from .models import Category, News , Contact
# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display=['title', 'slug', 'publish_time', 'status']
    list_filter=['publish_time', 'status']
    prepopulated_fields={"slug":("title", )}
    date_hierarchy='publish_time'
    search_fields=['title', 'body']
    ordering=['status', 'publish_time']

class CategoryAdmin(admin.ModelAdmin):
    list_display=['id', 'name']
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Contact)



