from django.contrib.auth import logout
from quantumapp.settings import REACT_APP_FORUM_URL, REACT_APP_HOME, REACT_APP_USER_PROFILE
from django.http import HttpResponseRedirect


def logout_user(request):
    # logout(request)
    return HttpResponseRedirect(REACT_APP_FORUM_URL)

def redirect_home(request):
    logout(request)
    return HttpResponseRedirect(REACT_APP_HOME)

def redirect_profile(request):
    logout(request)
    return HttpResponseRedirect(REACT_APP_USER_PROFILE)
