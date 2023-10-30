from django.urls import path, re_path
from .views import *
from .models import *

from django.views.decorators.cache import cache_page # импортируем декоратор 
#для кэширования отдельного представления

urlpatterns = [

    path('', BoardList.as_view(), name = 'home' ),
    re_path(r'^index/', BoardList.as_view(), name = 'home'),
    
    path('search', SearchList.as_view(), name = 'search' ),

    path('<int:pk>', PostDetail.as_view(), name = 'o_post'),
   
    path('add_post/', AddPostCreate.as_view(), name = 'add_post' ),
    path('update_post/<int:pk>/', PostUpdateView.as_view(), name = 'edit_post'),
   
    path('<int:pk>/like/', AddLikePost.as_view(), name = 'l_post'),
    
    path('<int:pk>/dislike/', AddDisPost.as_view(), name = 'd_post'),

    path('<int:pk>/like_com/', AddLikeCom.as_view(), name = 'l_com'),
    
    path('<int:pk>/dislike_com/', AddDisCom.as_view(), name = 'd_com'),

    path('profile/<int:pk>', ProfileDetail.as_view(), name = 'profile'),
    path('edit_profile/<int:pk>', EditProfile.as_view(), name = 'edit_profile'),

    path('comment/<int:pk>', commentForUser, name ='com_pr'),
    path('comment_del/<int:pk>', commentDel, name ='com_del'),
   
]