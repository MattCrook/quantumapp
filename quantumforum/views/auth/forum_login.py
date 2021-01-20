from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth import login, admin
from quantumforum.models import LoginForm
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.messages import error, success, INFO
from rest_auth.models import TokenModel
from quantumapp.settings import REACT_APP_FORUM_URL
from django.contrib.auth import get_user_model
import json

# We know the user is already authenticted with auth0, so there is no way to get to this point
# without going thru auth0 first from the FE. 

def login_user(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # login_form.save()
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            UserModel = get_user_model()

            user = UserModel.objects.get(email=email)
            # Maybe add check here for username as well.
            auth0_uid = user.auth0_identifier
            password = user.auth0_identifier.split('.')[1]

            # remote user authentication
            # authenticated_user = authenticate(remote_user=auth0_uid)

            authenticated_user = authenticate(request, username=auth0_uid, password=password)
            if authenticated_user is not None:
                token = TokenModel.objects.get(user=authenticated_user)
                # data = json.dumps({"valid": True, "token": token.key})
                login(request, authenticated_user)
                return redirect(reverse('quantumforum:group_chat'))
            else:
                print("LOGINDATA", login_form.errors.as_data())
                error_message = login_form.errors.as_data()
                messages.add_message(request, messages.ERROR, error_message)
                return redirect(reverse('quantumforum:login'))
        else:
            print("LOGINDATA2", login_form.errors.as_data())
            error_message = login_form.errors.as_data()
            messages.add_message(request, messages.ERROR, error_message)
            return redirect(reverse('quantumforum:login'))


    else:
        login_form = LoginForm()
        template = 'login.html'
        context = {
            'login_form': login_form,
            'CLIENT_URL': REACT_APP_FORUM_URL,
        }
        return render(request, template, context)
