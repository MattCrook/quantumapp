from quantumapi.views.auth.management_api_services import management_api_oath_endpoint, get_management_api_user, get_open_id_config, management_api_openid_authorization_codes
from quantumapp import settings
from quantumapi.models import UserProfile
from quantumadminapp.views import index

from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, HttpResponseRedirect
import json

from rest_auth.models import TokenModel
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer




# @api_view(['GET, POST'])
@csrf_exempt
def register_admin_user(request):
    try:
        if request.method == 'POST':
            req_body = json.loads(request.body.decode())
            UserModel = get_user_model()
            admin_user = UserModel.objects.get(email=req_body['email'])
            # Old password important. Means User can only use this once, and change password once.
            # Once they change their password, the auth0 id will no longer match.
            raw_password = req_body['oldPassword']
            is_valid_username = req_body['username'] == admin_user.auth0_identifier

            if admin_user.auth0_identifier == 'auth0|' + raw_password and is_valid_username:
                new_password = req_body['newPassword']
                admin_user.set_password(new_password)
                admin_user.save()

                new_userprofile = UserProfile.objects.create(
                address="1234 Quantum Ave",
                user=admin_user
                )
                new_userprofile.save()

                authenticated_user = authenticate(auth0_identifier=req_body['username'], password=new_password)
                if authenticated_user is not None:
                    token = TokenModel.objects.create(user=authenticated_user)
                    management_api_oauth_endpoint_result = management_api_oath_endpoint(settings.AUTH0_DOMAIN)
                    management_api_token = json.loads(management_api_oauth_endpoint_result)
                    management_api_jwt = management_api_token['access_token']
                    management_api_admin_user = get_management_api_user(settings.AUTH0_DOMAIN, management_api_jwt, authenticated_user.auth0_identifier.replace(".", "|"))
                    openid_endpoint = get_open_id_config(settings.AUTH0_DOMAIN, management_api_jwt)
                    # Logging in creates a session. need this as get_user_from_token endpoint currently looks at the request.session to grab the user_id
                    login(request, authenticated_user, backend='quantumapi.auth0_backend.QuantumAdminOpenID')

                    data = {
                        "valid": True,
                        "token": token.key,
                        "email": admin_user.email,
                        "first_name": admin_user.first_name,
                        "last_name": admin_user.last_name,
                        "username": admin_user.username,
                        "auth0_identifier": admin_user.auth0_identifier,
                        "user_profile_id": new_userprofile.id,
                        "is_staff": admin_user.is_staff,
                        "is_superuser": admin_user.is_superuser,
                        "management_api_token": management_api_token,
                        "management_jwt": management_api_jwt,
                        "id_token": management_api_jwt,
                        "management_user": management_api_admin_user
                    }
                    return HttpResponse(json.dumps(data), content_type='application/json')
                else:
                    data = json.dumps({"valid": False})
                    return HttpResponse(data, content_type='application/json')
            else:
                data = json.dumps({"valid": False, "error": "Auth credentials do not match."})
                return HttpResponse(data, content_type='application/json')

        # else:
        #     # A GET on page refresh. Either do a error page, or get this form page, or get redirect to index again to let react route it.
        #     pass

    except Exception as ex:
        error = json.dumps({"error": ex})
        return HttpResponse(error, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
