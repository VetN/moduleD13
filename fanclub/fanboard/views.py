from typing import Any, Dict
from django.http import  JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve, reverse
from django.views import View

from fanclub.settings import DEFAULT_FROM_EMAIL

from .filter import PostFilter
from django.core.paginator import Paginator
from .forms import AddPostForm,CommentForm, AddProfileForm
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from datetime import datetime
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


all=Post.objects.all()
Tn=Post.objects.all().filter(category='Tn')       
Hl=Post.objects.all().filter(category='Hl')     
DD=Post.objects.all().filter(category='DD')
DR=Post.objects.all().filter(category='DR')
GM=Post.objects.all().filter(category='GM')     
QG=Post.objects.all().filter(category='QG')      
BS=Post.objects.all().filter(category='BS') 
LW=Post.objects.all().filter(category='LW')    
PM=Post.objects.all().filter(category='PM')    
SM=Post.objects.all().filter(category='SM')
  
cat = { 'ВСЕГО ОБЪЯВЛЕНИЙ': all.count(),
        'Танки': Tn.count(),
        'Хилы': Hl.count(),
        'ДД': DD.count(),
        'Торговцы': DR.count(),
        'Гилдмастеры': GM.count(),
        'Квестгиверы': QG.count(),
        'Кузнецы': BS.count(),
        'Кожевники': LW.count(),
        'Зельевары': PM.count(),
        'Мастера Заклинаний': SM.count(),
     
        }


class BoardList(ListView):
    model = Post 
    template_name = 'flatpages/index.html' 
    context_object_name = 'board' 
 
    ordering = ['-dataCreation']
    paginate_by = 9

     # считаем количество комментариев под постом (важно чтобы работало перебор на странице должен быть сделан так(board))
    queryset  = Post.objects.annotate(com_count = Count('comment'))


    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['cat']=cat
        context['all'] = Post.objects.all().count()

        return context
    



# страница поста с возможностью комментировать зарегистрир. юзерам
# LoginRequiredMixin,
class PostDetail( DetailView, FormMixin):
    model = Post
    template_name = 'flatpages/one_post.html' 
    context_object_name = 'one_post'
    queryset = Post.objects.all()
    
    # код добавления комментов под постом
    # код для автомат заполнения строки commentPost и commentUser
    # изменение вида формы в несколько этапов
    # 1 получаем форму проверяем валидность
    form_class = CommentForm
  
    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    # присваиваем строкам значения
    # дополнительно проводим проверку на регистрацию ( чтобы комментарий писал зарегистриров пользователь)
    def form_valid(self, form):
        if not self.request.user.is_anonymous:
            comm = form.save(commit=False)
            comm.commentUser = self.request.user
            comm.commentPost = Post.objects.get(id=self.kwargs['pk'])
            comm.save()
            return super().form_valid(form)
        else:
            return redirect ('sign:signup')
    
    
    
    # 3 переход после заполнения формы(FormMixin) 
    def get_success_url(self, **kwargs):
        return reverse('o_post', args=[self.kwargs['pk']]) 


    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['cat']=cat
        

        # список комментариев под постом c проверкой на подтверждение
        self.id = resolve(self.request.path_info).kwargs['pk'] 
        context['comment_post'] = Comment.objects.order_by('-dataCreation').filter(commentPost_id = self.id).filter(approved_comment='1')
        
        context['comments'] = Comment.objects.order_by('-dataCreation').filter(commentUser_id=self.id)
        
        # провекрка на нажатии кнопки like-dislike(AddLikePost and AddDisPost)
        post= Post.objects.get(id=self.id)
        li_all = post.like_post.all()
        is_li=False
        for li in li_all:
            
            if li == self.request.user:
                is_li = True
                print (is_li)
                context['mark_li'] = '_pr'
                context['mark_dli'] = ''
                break
            else:
                context['mark_li'] = ''
                context['mark_dli'] = '_pr'

        return context

class AddLikePost(View):
   
    def post(self, request, pk,  *args, **kwargs):
        post= Post.objects.get(pk=pk)
        user=request.user
        print("addlikepost", post)
        is_dli =False
        dli_all = post.dislike_post.all()
        for dli in dli_all:
            if dli == user:
                is_dli = True
                break

        if is_dli:
            post.dislike_post.remove(user)
            post.like()
           
        is_li = False
        li_all = post.like_post.all()
       
        for li in li_all:
            if li == user:
                is_li = True
                break

        if not is_li:
            mark_li = '_pr'
            post.like_post.add(user)
            post.like()

        if is_li:
            mark_li = ''
            post.like_post.remove(user)
            post.dislike()

        def make_json():
            post2 = Post.objects.get(pk=pk)
            return JsonResponse(
                {'likes_count': post2.like_post.count(), 
                 'dislikes_count': post2.dislike_post.count(), 
                 'myid': post2.id,  'mark_li': mark_li, 'mark_dli': ''
                 })
        return make_json()

        

class AddDisPost(View):
    def post(self, request, pk,  *args, **kwargs):
        post= Post.objects.get(pk=pk)
        user=request.user
        
        is_li = False
        li_all = post.like_post.all()
    
        print('adddislikepost')
        for li in li_all:
            if li == user:
                is_li = True
                break
        
        if is_li:
            post.like_post.remove(user)
            post.dislike()
        is_dli = False
        dli_all = post.dislike_post.all()
        
        for dli in dli_all:
            if dli == user:
                is_dli = True
                break
        
        if not is_dli:
            mark_dli = '_pr'
            post.dislike_post.add(user)
            post.dislike()
        if is_dli:
            mark_dli = ''
            post.dislike_post.remove(user)
            post.like()
    
        def make_json():
            post2 = Post.objects.get(pk=pk)
            return JsonResponse(
                {'likes_count': post2.like_post.count(), 
                 'dislikes_count': post2.dislike_post.count(), 
                 'myid': post2.id, 'mark_li': '', 'mark_dli': mark_dli
                 })
        return make_json()
        

class AddLikeCom(View):
  
    def post(self, request, pk,  *args, **kwargs):
       
        comment= Comment.objects.get(pk=pk)
        user=request.user
    
        is_dcom =False
        dcom_all = comment.dislike_com.all()
        for dcom in dcom_all:
            if dcom == user:
                is_dcom = True
                break

        if is_dcom:
            comment.dislike_com.remove(user)
            comment.like()
        is_com = False
        com_all = comment.like_com.all()
       
        for com in com_all:
            if com == user:
                is_com = True
                break

        if not is_com:
            comment.like_com.add(user)
            comment.like()

        if is_com:
            comment.like_com.remove(user)
            comment.dislike()
        return redirect(request.META.get('HTTP_REFERER'))

class AddDisCom(View):
    def post(self, request, pk,  *args, **kwargs):
        comment= Comment.objects.get(pk=pk)
        user=request.user
        
        is_com = False
        com_all = comment.like_com.all()
    
   
        for com in com_all:
            if com == user:
                is_com = True
                break
        
        if is_com:
            comment.like_com.remove(user)
            comment.dislike()
        is_dcom = False
        dcom_all = comment.dislike_com.all()
        
        for dcom in dcom_all:
            if dcom == user:
                is_dcom = True
                break
        
        if not is_dcom:
            comment.dislike_com.add(user)
            comment.dislike()
        if is_dcom:
            comment.dislike_com.remove(user)
            comment.like()
        return redirect(request.META.get('HTTP_REFERER'))
    
    


       

class SearchList(ListView):
    model = Post  
    template_name = 'flatpages/search.html'  
    context_object_name = 'search' 
    ordering = ['-dataCreation']
    queryset = Post.objects.order_by('-id')
    paginate_by = 4
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        context['cat']=cat
        
        return context
    

    
   
    

class AddPostCreate(LoginRequiredMixin, CreateView):
    template_name = 'flatpages/add_post.html' 
    form_class = AddPostForm
    success_url = '/'
    
    # автоматическое добавление юзера
    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            add_post = form.save(commit=False)
            add_post.author = Profile.objects.get(id=self.request.user.id)
            add_post.save()
            
           
    
 
class PostUpdateView( UpdateView):   
    template_name = 'flatpages/add_post.html'
    form_class = AddPostForm
    success_url = '/user/personal'

         # метод get_object мы используем вместо queryset, 
         # чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
            
    

class ProfileDetail( DetailView):
    model = Profile
    template_name = 'flatpages/profile.html'
    context_object_name = 'profile'
 
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['cat']=cat
        

        
        self.id = resolve(self.request.path_info).kwargs['pk'] 
        # список постов геймера
        context['post'] = Post.objects.order_by('-dataCreation').filter(author_id=self.id)
        
        # список комментариев геймера
        context['comments'] = Comment.objects.order_by('-dataCreation').filter(commentUser_id=self.id)
        
        # список комментариев к постам геймера принятые 
        context['com_post'] = Comment.objects.order_by('-dataCreation').filter(commentPost__author_id=self.id).filter(approved_comment='1')

        return context
   
class EditProfile(LoginRequiredMixin, UpdateView):
    template_name = 'flatpages/edit_profile.html' 
    form_class = AddProfileForm
    success_url = '/user/personal'

         # метод get_object мы используем вместо queryset, 
         # чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Profile.objects.get(pk=id)
    

def commentForUser (request, pk):
    comment_pr = Comment.objects.get(id=pk)
    post = comment_pr.commentPost

    # меняем значение на комментарий одобрен
    comment_pr.approved_comment=True
    comment_pr.save()
    
    # отсылаем письмо комментатору
    comm_user=comment_pr.commentUser
    email = comment_pr.commentUser.email

    html_content = render_to_string (  'mail/mail_comment_accept.html',
                                            {   'post': post,
                                                'comment': comment_pr,              # 'даем название использ в html' : 
                                                'user' : comm_user,},               # чтобы в письме отразить имя пользов
                                        )
    msg = EmailMultiAlternatives(
            subject=f'Сообщение об одобрении вашего комментария',# тема письма
            body='',
            from_email= DEFAULT_FROM_EMAIL, #так адрес возьмется из setting или прямо адрес писать 'petechka@yandex.ru',
            to=[email, ], # к email юзера через запятую можно добавить свою почту для проверки
    )
            
    msg.attach_alternative(html_content, "text/html") # (html, "text/html") добавляем html
    try:                # пытаемся отослать
            msg.send() # отсылаем    
    except Exception as e:
            print(e)

    return redirect(request.META.get('HTTP_REFERER'))


def commentDel(request, pk):
    comment_pr = Comment.objects.get(id=pk)
    comment_pr.delete()
    
    email = comment_pr.commentUser.email
    post = comment_pr.commentPost
    comm_user=comment_pr.commentUser
    
    msg = EmailMultiAlternatives(
            subject=f'Ваш комментарий отклонен',# тема письма
            body= 'Ваш комментарий к посту {post.title}  отклонен автором',
            from_email= DEFAULT_FROM_EMAIL, #так адрес возьмется из setting или прямо адрес писать 'petechka@yandex.ru',
            to=[email, ], # к email юзера через запятую можно добавить свою почту для проверки
    )
    html_content = render_to_string (  'mail/mail_comment_del.html',
                                            {   'post': post,
                                                'comment': comment_pr,                                     
                                                'user' : comm_user,},               
                                        )        
    msg.attach_alternative(html_content, "text/html") 
    try:               
            msg.send()    
    except Exception as e:
            print(e)

    return redirect(request.META.get('HTTP_REFERER'))


