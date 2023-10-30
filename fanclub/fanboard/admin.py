from django.contrib import admin
from django.contrib import admin
from .models import  Profile, Post, Comment
# Register your models here.

admin.site.register(Profile)    



    # list_display — это список или кортеж со всеми полями, 
    # которые вы хотите видеть в таблице
#@admin.register(Profile)
#class ProfileAdmin(admin.ModelAdmin):
    #list_display = ["username", "first_name", "last_name", "email"]
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["author","title", "dataCreation", "category", "rating"]
    list_filter = ['author','dataCreation', 'rating', "category"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["commentPost", "commentUser", "dataCreation", "rating"]


