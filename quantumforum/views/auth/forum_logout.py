from django.contrib.auth import logout
from quantumapp.settings import REACT_APP_FORUM_URL
from django.http import HttpResponseRedirect


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(REACT_APP_FORUM_URL)
