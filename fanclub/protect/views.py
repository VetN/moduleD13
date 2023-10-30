from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import resolve
from fanboard.models import *
from django.core.paginator import Paginator


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/user_page.html'
    paginate_by = 2
    paginate_by_com = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        
        p_user= Profile.objects.get(user_id=self.request.user)
        
        
        post_user = Post.objects.order_by('-dataCreation').filter(author=p_user)
        comments_user = Comment.objects.order_by('-dataCreation').filter(commentUser_id=p_user.id)
        com_post_pr = Comment.objects.order_by('-dataCreation').filter(commentPost__author_id=p_user.id).filter(approved_comment='1')
      
        
      
        context['post_user'] = post_user
        context['comments_user']= comments_user
        context['com_post_pr'] = com_post_pr
        context['com_post_needpr']  = Comment.objects.order_by('-dataCreation').filter(commentPost__author_id=p_user.id).filter(approved_comment='0')

        # пагинация постов
        p= Paginator(post_user, self.paginate_by)
        page_number = self.request.GET.get('page')
        context['post_user_p']= p.get_page(page_number)

        # пагинация комментов
        p_1= Paginator(com_post_pr, self.paginate_by_com)
        context['com_post_pr_p'] = p_1.get_page(page_number)
        
        # пагинация комментов
        p_2= Paginator(comments_user, self.paginate_by_com)
        context['comments_user_p'] = p_2.get_page(page_number)
        

        #self.id = resolve(self.request.path_info).kwargs['pk'] 
        return context
  


