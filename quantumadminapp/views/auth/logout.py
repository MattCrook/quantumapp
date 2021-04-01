from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def logout_admin_user(request):
    auth_views.auth_logout(request)
    return HttpResponseRedirect("/quantumadmin/")
