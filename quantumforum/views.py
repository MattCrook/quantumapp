from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quantumapi.models import Credential, Messages

def index(request):
    template = 'forum/index.html'
    context = {}
    return render(request, template, context)


def room(request, room_name):
    if room_name == 'private_message':
        if request.COOKIES and request.COOKIES['session']:
            messages = Messages.objects.all()
            template = 'private_message/private_message.html'
            context = {
                'room_name': room_name,
                'messages': messages,
            }
    else:
        template = 'errors/error.html'
        error = 'Oops! Something went wrong.'
        context = {
            'error': error,
        }
    return render(request, template, context)


# def general_chat_room(request):
#     template = 'general/general.html'
#     room_name = 'general'
#     context = {
#         'room_name': room_name
#     }
#     return render(request, template, context)
