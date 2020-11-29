from quantumapi.models import User as UserModel
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm




class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserModel
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'auth0_identifier', )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'auth0_identifier', )



# From for Register
# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(max_length=50)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', )
