from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from quantumapp import settings
from django.http import HttpResponseRedirect
from urllib.parse import urlencode

# logout method to clear the session and redirect the user to the Auth0 logout endpoint.
def auth0_logout(request):
    # user = request.user
    logout(request)
    auth_views.auth_logout(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)

def logout_user(request):
    # user = request.user
    logout(request)
    return HttpResponseRedirect("/")
