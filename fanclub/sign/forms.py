from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # не забываем импортировать класс формы аутентификации
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm, BaseSignupForm, LoginForm



#class RegisterForm(UserCreationForm):
  # password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='ПА')
  # password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')
  
  # class Meta:
   #    model = User
    #   fields = (
      #   "username", # опционально
        
      #   "email",
      #   "password1",
      #   "password2",
      #     )
      # widgets = {
         #  'username': forms.TextInput(attrs={'class': 'form-control'}),
           #'first_name': forms.TextInput(attrs={'class': 'form-control'}),
         #  'email': forms.EmailInput(attrs={'class': 'get-started-btn_1 scrollto'}),
     #  }
      
    

# Добавляем новую форму для аутентификации пользователя
# Добавляем новую форму для аутентификации пользователя
#class LoginForm(AuthenticationForm):
    #class Meta:
      #  model = User
      #  fields = (
        # "username",
       #  "password",
     #      )
      #  widgets = {
           #'username': forms.TextInput(attrs={'class': 'my_form'}),
            #'first_name': forms.TextInput(attrs={'class': 'form-control'}),
       #    'email': forms.EmailInput(attrs={'class': 'get-started-btn_1 scrollto'}),
    #   }
#    def clean(self):
 #      username = self.cleaned_data.get('username')
 #      email = self.cleaned_data.get('email')
 #      if User.objects.filter(username=username).exists():
 #          raise forms.ValidationError("Пользователь с таким ником уже существует")
 #      if User.objects.filter(email=email).exists():
 #          raise forms.ValidationError("Пользователь с таким email уже существует")
 #      return super().clean()


 # изменение полей формы при регистрации allauth       
class CommonSignupForm(SignupForm, BaseSignupForm):
       
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[("password1")] = forms.CharField(widget=forms.PasswordInput(attrs={'class':'my_formlogin_2' }),
                                                     required=True, label=("ПАPОЛЬ"), )
        self.fields[("password2")] = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'my_formlogin_2'}),
                                                     required=True, label=("ПАРОЛЬ"), )
        self.fields[("username")] = forms.CharField(widget=forms.TextInput(attrs={'class': 'my_formlogin_3'}),
                                                     required=True, label=("НИК"), )
        self.fields[("first_name")] = forms.CharField(widget=forms.TextInput(attrs={'class': 'my_formlogin_3'}),
                                                     required=True, label=("ИМЯ"), )
        self.fields[("last_name")] = forms.CharField(widget=forms.TextInput(attrs={'class': 'get-started-btn_2 scrollto'}),
                                                     required=True, label=("ФАМИЛИЯ"), )
        self.fields[("email")] = forms.CharField(widget=forms.TextInput(attrs={'class': 'my_formlogin_1'}),
                                                    required=True, label=("E-mail"), )



 

class CommonLoginForm(LoginForm):
       
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                'class': 'my_formlogin',
                                                                 'placeholder': 'Введите пароль'}),
                                                                required=True, label=("ПАРОЛЬ"), )

     
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"] =forms.EmailField(widget=forms.TextInput(attrs={'class': 'my_formlogin_1',
                                                                               'placeholder': 'адреc почты'}),
                                                                            required=True, label=("E-mail"), ) 
    
    

    
    def save(self, request):
        user = super(CommonLoginForm, self).save(request)
        #user.username = self.cleaned_data['username']
        user.password = self.cleaned_data['password']
        user.login= self.cleaned_data['email']
        user.save()
        return user