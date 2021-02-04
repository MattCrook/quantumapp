from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import login, admin
from quantumforum.models import LoginForm
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.messages import error, success, INFO
from rest_auth.models import TokenModel
from quantumapp.settings import REACT_APP_FORUM_URL, SOCIAL_AUTH_LOGIN_REDIRECT_URL, AUTH0_DOMAIN
from django.contrib.auth import get_user_model
import json

from social_django.views import auth, do_auth, complete, do_complete
from social_django.context_processors import backends, user_backends_data, login_redirect
from social_core.actions import user_is_authenticated

from quantumapi.views.auth.management_api_services import get_open_id_config, management_api_oath_endpoint, get_management_api_grants, get_management_api_client_grants, get_management_api_connections, retrieve_user_logs

# We know the user is already authenticted with auth0, so there is no way to get to this point
# without going thru auth0 first from the FE.

def login_user(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            # password = login_form.cleaned_data.get('password')

            oauth_endpoint = management_api_oath_endpoint(AUTH0_DOMAIN)
            management_api_token = json.loads(oauth_endpoint)
            token = management_api_token['access_token']
            open_id_config = get_open_id_config(AUTH0_DOMAIN, token)
            grants = get_management_api_grants(AUTH0_DOMAIN, token)
            client_grants = get_management_api_client_grants(AUTH0_DOMAIN, token)
            connections = get_management_api_connections(AUTH0_DOMAIN, token)

            try:
                UserModel = get_user_model()
                user = UserModel.objects.get(email=email)
                password = user.auth0_identifier.split(".")[1]

                user_logs = retrieve_user_logs(AUTH0_DOMAIN, token, user.auth0_identifier.replace(".", "|"))
                social_account = user.socialaccount_set.get(user_id=user.id)
                social_token = social_account.socialtoken_set.get(account_id=social_account.pk).token_secret
                # social_storage = user.storage.user.tokens

                auth0_uid = user.auth0_identifier
                password = user.auth0_identifier.split('.')[1]

                # remote user authentication
                # remote_authenticated_user = authenticate(remote_user=auth0_uid)

                authenticated_user = authenticate(request, username=auth0_uid, password=password)
                # backend_data = backends(request)
                # auth0_backend = backend_data['backends']['backends'][1]
                # openid_backend = backend_data['backends']['backends'][0]
                # social_auth = auth(request, auth0_backend)
                # social_complete = do_complete(request.backend, login, authenticated_user)

                token = TokenModel.objects.get(user=authenticated_user)

                if token is not None:
                    authenticated_social_user = authenticated_user.social_auth.get(provider='auth0')
                    social_user = user.social_auth.get(user_id=user.id)
                    is_authenticated = user_is_authenticated(authenticated_user)

                    # Second check/ validation to ensure the user is who they say they are and is a match.
                    if authenticated_social_user.uid == social_user.uid and is_authenticated:
                        return redirect(reverse('social:begin', kwargs={'backend': 'auth0'}))
                        # login(request, authenticated_user, request.backend.name)


                    else:
                        print("LOGINDATA2", login_form.errors.as_data())
                        error_message = login_form.errors.as_data()
                        messages.add_message(request, messages.ERROR, error_message)
                        return redirect(reverse('quantumforum:login'))
                else:
                    print("LOGINDATA3", login_form.errors.as_data())
                    error_message = "Incorrect Email or Password."
                    messages.add_message(request, messages.ERROR, error_message)
                    return redirect(reverse('quantumforum:login'))
            except Exception as ex:
                error_message = "Incorrect Email or Password."
                messages.add_message(request, messages.ERROR, error_message)
                print(ex.args)
                return redirect(reverse('quantumforum:login'))
        else:
            print("LOGINDATA4", login_form.errors.as_data())
            error_message = login_form.errors.as_data()
            messages.add_message(request, messages.ERROR, error_message['email'][0])
            return redirect(reverse('quantumforum:login'))

    else:
        login_form = LoginForm()
        template = 'login.html'
        context = {
            'login_form': login_form,
            'CLIENT_URL': REACT_APP_FORUM_URL,
        }
        return render(request, template, context)



##################################################################################################

        # complete_uri = social_auth.url
        # if 'redirect_uri' in complete_uri:
            # redirect_uri_index = complete_uri.index('redirect_uri')
            # authorize_endpoint = complete_uri[:redirect_uri_index]  # get the first half of uri
            # redirect_uri = complete_uri[redirect_uri_index:]  # get the rest half of uri
            # redirect_uri = complete_uri[complete_uri.index('localhost:8000') + 14:]
            # state = redirect_uri[redirect_uri.index('state=') + 6:redirect_uri.index('response_type=') - 1]

        # backend_data = backends(request)
        # auth0_backend = backend_data['backends']['backends'][1]
        # openid_backend = backend_data['backends']['backends'][0]

        # social_auth = auth(request, auth0_backend)
        # social_complete = complete(request, request.backend)
        # response_url = social_auth.url

        # backend_data = backends(request)
        # user_backend = authenticated_user.backend
        # storage = authenticated_user.storage
        # backends_data = user_backends_data(authenticated_user, backend_data, storage)

        # login(request, authenticated_user, request.backend.name)
        # return redirect(reverse('social:complete'), kwargs={"backend": request.backend})

        # login(request, authenticated_user, request.backend.name)
        # login_redirect_uri = login_redirect(request)
        # return redirect(reverse('quantumforum:index'))
        # return redirect(login_redirect_uri)
        # return redirect(redirect_uri, kwargs={'backend': request.backend.name})
