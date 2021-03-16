from quantumapi.views.auth.management_api_services import management_api_oath_endpoint
from quantumapp import settings
from quantumapi.models import UserProfile

from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import json

from rest_auth.models import TokenModel




@csrf_exempt
def register_admin_user(request):
    try:
        if request.method == 'POST':
            req_body = json.loads(request.body.decode())
            UserModel = get_user_model()
            admin_user = UserModel.objects.get(auth0_identifier=req_body['email'])
            raw_password = req_body['oldPassword']

            if admin_user.auth0_identifier == raw_password:
                new_password = req_body['newPassword']
                admin_user.set_password(new_password)
                admin_user.save()

                new_userprofile = UserProfile.objects.create(
                address="1234 Quantum Ave",
                user=admin_user
                )
                new_userprofile.save()

                authenticated_user = authenticate(auth0_identifier=req_body['oldPassword'], password=new_password)
                if authenticated_user is not None:
                    token = TokenModel.objects.create(user=authenticated_user)

                    data = {
                        "valid": True,
                        "token": token.key,
                        "first_name": admin_user.first_name,
                        "last_name": admin_user.last_name,
                        "username": admin_user.username,
                        "auth0_identifier": admin_user.auth0_identifier,
                        "user_profile_id": new_userprofile.id,
                        "is_staff": admin_user.is_staff,
                        "is_superuser": admin_user.is_superuser,
                    }
                    return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                data = json.dumps({"valid": False})
                return HttpResponse(data, content_type='application/json')

        else:
            # A GET on page refresh. Either do a error page, or get this form page, or get redirect to index again to let react route it.
            pass

    except Exception as ex:
        error = json.dumps({"error": ex})
        return HttpResponse(error, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
