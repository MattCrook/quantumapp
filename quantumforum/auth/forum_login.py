from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth import login, admin
from quantumforum.models import LoginForm
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.messages import error, success, INFO
from rest_auth.models import TokenModel
import json



def forum_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user is not None:
            token = TokenModel.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            login(request, authenticated_user)
            return redirect(reverse('quantumforum:group_chat'))
        else:
            data = json.dumps({"valid": False})
            # return HttpResponse(data, content_type='application/json')
            print("LOGINDATA", login_form.errors.as_data())
            error_message = login_form.errors.as_data()
            messages.add_message(request, messages.ERROR, error_message)
            return redirect(reverse('quantumforum:login'))

    else:
        form = LoginForm()
        template = 'registration/login.html'
        context = {
            'form': form
        }
        return render(request, template, context)
