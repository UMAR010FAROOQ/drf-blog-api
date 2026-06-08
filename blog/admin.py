from urllib import request

from django.contrib import admin
from .models import Category, Post, Comment

# Register your models here.
# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'is_deleted', 'created_at')
    list_filter = ('is_published', 'is_deleted', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

    actions = ['restore_posts', 'soft_delete_posts']  # 👈 ADD THIS

    def restore_posts(self, request, queryset):
        queryset.update(is_deleted=False)
        self.message_user(request, "Selected posts restored successfully")

    restore_posts.short_description = "Restore selected posts"

    def soft_delete_posts(self, request, queryset):
        queryset.update(is_deleted=True)
        self.message_user(request, "Selected posts soft deleted successfully")

    soft_delete_posts.short_description = "Soft delete selected posts"
    

admin.site.register(Category)
admin.site.register(Comment)

