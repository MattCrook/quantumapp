import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from quantumapi.models import UserProfile, Image, ImageForm


@csrf_exempt
def register_user(request):
    print("IN REGISTER", request)
    form_data = request.POST
    print("FORMDATA", form_data)

    # Load the JSON string of the request body into a dict
    # req_body = json.loads(request.body.decode())
    # print(req_body)

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    try:
        new_user = User.objects.create_user(
            username=form_data['username'],
            email=form_data['email'],
            password=form_data['password'],
            first_name=form_data['first_name'],
            last_name=form_data['last_name']
        )
        new_user.save()

        image = ImageForm()
        img_obj = image.instance
        img_obj.image = request.FILES["image"]
        img_obj.save()

        new_userprofile = UserProfile()
        new_userprofile.user_id = new_user.id
        new_userprofile.image_id = img_obj.id
        new_userprofile.credits = form_data["credits"],
        new_userprofile.address = form_data["address"]

        new_userprofile.save()

        # new_userprofile = UserProfile.objects.create(
        #     user=new_user,
        #     image=image,
        #     credits=req_body["credits"],
        #     address=req_body["address"]
        # )

        # Commit the user to the database by saving it
        # new_userprofile.save()
        print("NEWUSERPROFILE", new_userprofile)
        print("NEWUSER2", new_user)
        print("IMAGEOBJ", image)


        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=new_user)

        # Return the token to the client
        data = json.dumps({"token": token.key})
        return HttpResponse(data, content_type='application/json')

    except Exception as x:
        return HttpResponse(x, content_type='application/json')
