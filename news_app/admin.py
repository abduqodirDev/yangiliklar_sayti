from django.contrib import admin
from .models import Category, News , Contact, Comment
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

class CommentAdmin(admin.ModelAdmin):
    list_display=['user', 'body', 'created_time', 'active']
    list_filter=['active', 'created_time']
    search_fields=['user', 'body']
    actions=['disable_comments', 'activate_comments']
        
    def disable_comments(self, request, queryset):
        queryset.Update(active=False)
    
    def activate_comments(self, request, queryset):
        queryset.Update(active=True)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Contact)
admin.site.register(Comment, CommentAdmin)


