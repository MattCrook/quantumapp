import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from quantumapi.models import UserProfile, Image


@csrf_exempt
def register_user(request):

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    try:
        new_user = User.objects.create_user(
            username=req_body['username'],
            email=req_body['email'],
            password=req_body['password'],
            first_name=req_body['first_name'],
            last_name=req_body['last_name']
        )
        new_user.save()

        new_image = Image()
        new_image.image = request.data["image"]
        new_image.save()

        new_userprofile = UserProfile()
        new_userprofile.address=req_body['address'],
        new_userprofile.image=new_image
        new_userprofile.user=new_user,

        # Commit the user to the database by saving it
        new_userprofile.save()
        print(new_userprofile)
        print(new_image)
        print(new_user)


        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=new_user)

        # Return the token to the client
        data = json.dumps({"token": token.key})
        return HttpResponse(data, content_type='application/json')

    except Exception as x:
        return HttpResponse(x, content_type='application/json')
