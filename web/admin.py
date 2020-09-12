from django.contrib import admin

from .models import Account, Comment, Keyword, Post, Update

# Register your models here.


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['owner', 'uid', 'username', 'full_name', 'url', 'biography', 'external_url', 'pic_url']
    list_display_links = ['owner', 'uid', 'username', 'full_name', 'url', 'biography', 'external_url', 'pic_url']
    search_fields = ['owner', 'uid', 'username', 'full_name', 'url', 'biography', 'external_url', 'pic_url']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['owner', 'username', 'timestamp', 'uid', 'url', 'text', 'pic_url']
    list_display_links = ['owner', 'username', 'timestamp', 'uid', 'url', 'text', 'pic_url']
    search_fields = ['owner', 'username', 'timestamp', 'uid', 'url', 'text', 'pic_url']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['owner', 'post', 'timestamp', 'uid', 'replay_uid', 'username', 'text', 'match', 'read']
    list_display_links = ['owner', 'post', 'timestamp', 'uid', 'replay_uid', 'username', 'text', 'match', 'read']
    search_fields = ['owner', 'post', 'timestamp', 'uid', 'replay_uid', 'username', 'text', 'match', 'read']


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ['owner', 'name']
    list_display_links = ['owner', 'name']
    search_fields = ['owner', 'name']


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ['owner', 'last']
    list_display_links = ['owner', 'last']
    search_fields = ['owner', 'last']
