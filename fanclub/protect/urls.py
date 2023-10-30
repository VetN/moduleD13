from django.urls import path
from .views import IndexView

app_name = 'protect'
urlpatterns = [
    path('personal', IndexView.as_view(), name='personal'),
    #path('upgrade/', upgrade_me, name = 'upgrade'),
    #path('upauthors/', upauthors, name = 'upauthors')
]