from django import forms 
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm, UsernameField


# class SignupForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['user', 'email', 'password']  # Include fields you want in the signup form

#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
        
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])  # Hash the password
#         if commit:
#             user.save()
#         return user
    
    
#     class Meta:
#         model = User 
#         fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
    
    username = UsernameField(label='Enter Username', widget=forms.TextInput)
    password = forms.CharField(label='Enter Password', widget=forms.PasswordInput)
    

# class LoginForm(forms.ModelForm):
#     template_name = "login.html"
    
#     class Meta:
#         model = CustomUser
#         fields = ['username','password']
    
    
    
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    
    # class Meta:
    #     model = User
    #     fields = ['username', 'password']
    # # username = forms.CharField(
    # #     max_length=150,
    # #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    # #     label='Username',
    # # )
    # # password = forms.CharField(
    # #     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    # #     label='Password',
    # # )