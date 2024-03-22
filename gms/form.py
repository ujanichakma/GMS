from django.contrib.auth.forms import AuthenticationForm 
# from .models import Teacher,Student
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label='Username'
        self.fields['password'].label='Password'
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username','class': 'form-control'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter your password','class': 'form-control'})




# class TeacherAuthForm(forms.ModelForm):
#     class Meta:
#         model=Teacher
#         fields=['username','password']
#         # labels={'username':'Enter Name'}
#         # help_text={'username':'Enter Username','password':'Enter Password'}
#         # error_messages={'username':{'required':'Username Required'}}
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}),
#         }


# class StudentAuthForm(AuthenticationForm):
#     class Meta:
#         model=Student
#         fields=('username','password')
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control'}),
#         }
    
    #  def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.fields['name'].widgets.attrs.update({'class': 'form-control'})
