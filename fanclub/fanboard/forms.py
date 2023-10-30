from django import forms
from django.forms import ModelForm
from .models import *

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       self.author = kwargs.pop('author', None)
       super(AddPostForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Post
        fields =['category', 'title', 'content', 'photo', 'video', 'file']

        


# создаем форму, чтобы использовать ее в detailviews
# возможность добавлять комментарии под постом и не заполнять строку commentPost и commentUser
class CommentForm(forms.ModelForm):
   def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user', None)
       super(CommentForm, self).__init__(*args, **kwargs)

   class Meta:
       model = Comment
       fields = [
           'content',
       ]

class AddProfileForm(forms.ModelForm):
   class Meta:
       model=Profile
       fields=['pro_photo', 'site', 'vk'] 
       