from django.contrib import admin

# Register your models here.
from .models import Story,Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display=['title','publish'] 
    search_fields=['title',] 
    class Media:
        js=('tiny.js',)  