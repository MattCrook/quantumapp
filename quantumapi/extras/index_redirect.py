from django.shortcuts import render
from quantumapp.settings import CLIENT_URL, FORUM_URL, ADMIN_URL




def index_redirect(request):
    if request.method == 'GET':
        # ToDo: Send api call to errors endpoint of user hitting this page - triggerd by status code
        template = "index_redirect.html"
        context = {
            'CLIENT_URL': CLIENT_URL,
            'FORUM_URL': FORUM_URL,
            'ADMIN_URL': ADMIN_URL
        }

        return render(request, template, context)
