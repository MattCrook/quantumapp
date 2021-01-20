from django import forms
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext, gettext_lazy as _





class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password',)







# class PasswordField(forms.CharField):
#     widget = forms.PasswordInput

# class PasswordModelField(models.CharField):

#     def formfield(self, **kwargs):
#         defaults = {'form_class': PasswordField}
#         defaults.update(kwargs)
#         return super(PasswordModelField, self).formfield(**defaults)

# class LoginForm(AuthenticationForm):
    # username = forms.CharField()
    # password = forms.PasswordInput(render_value=True)

    # class Meta:
    #     model = get_user_model()
        # fields = ('username', 'password')
