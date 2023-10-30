from django.shortcuts import render
from django.views.generic.edit import CreateView
#from .forms import RegisterForm
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from .forms import LoginForm, CommonSignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView




# регистрация с получением письма на почту по allauth
class RegisterView(CreateView):
    model = User
    form_class = CommonSignupForm
    template_name = 'sign/signup.html'
    success_url = '/'

# регистрация по одноразовому коду
# 1 создание кода и отправка на почту этого кода
#def register_log(request):
#   username=request.POST['username']
#   password = request.POST['password]
#   user = authenticate(request, username=username, password=password)
#   is user is not NONE:
#       OneTimeCode.objects.create(code=random.choice('abcde'), user=user) # модель одноразов кода, котор создается в момент отправления
#       определить время ожидания
#       return redirect ('/')# страница с сообщением, что отправлено письмо
#   else:
#       #error

# 2 проверка кода и если он подходит, то вход
#def lod_in(request):
#   username=request.POST['username']
#   code = request.POST['code']
#   if  OneTimeCode.objects.filter(code=code, user__username=username).exists():
#       login(request, user)
#   else:
#   #error

class LoginView(FormView):
    model = User
    form_class = LoginForm
    template_name = 'sign/login.html'
    success_url = '/user/personal/'
  
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username= username, password=password)
        if user is not None:
           login(self.request, user)
        return super().form_valid(form)
  
  
class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/logout.html'
    
   
    def get(self, request, *args, **kwargs):
       logout(request)
       return super().get(request, *args, **kwargs)
   
