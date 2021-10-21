from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.http import HttpResponse
# from django.conf import settings
# from .user import UserSerializer
from django.contrib.auth import get_user_model
from quantumapi.models import UserProfile, Credit, Image, User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        # url = serializers.HyperlinkedIdentityField(view_name='userprofile', lookup_field='id')
        fields = ('id', 'address', 'image', 'credits', 'user', )
        depth = 2
        # extra_kwargs = {'password': {'write_only': True}}


class UserProfiles(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]


    def list(self, request):
        try:
            userprofiles = UserProfile.objects.all()

            email = self.request.query_params.get('email', None)
            user_id = self.request.query_params.get('userId', None)

            # email = self.request.GET.get('email', None)
            # user_id = self.request.GET.get('user_id', None)
            # email = self.request.resolver_match.kwargs.get('email', None)
            # user_id = self.request.resolver_match.kwargs.get('user_id', None)


            if email is not None:
                userprofiles = UserProfile.objects.filter(user_id=request.user.id)
                # serializer = UserProfileSerializer(userprofile, context={'request': request})

            if user_id is not None:
                userprofiles = UserProfile.objects.filter(user_id=request.user.id)
                # serializer = UserProfileSerializer(userprofile, context={'request': request})

            serializer = UserProfileSerializer(userprofiles, many=True, context={'request': request})
            return Response(serializer.data)

        except:
            if UserProfile.DoesNotExist:
                return HttpResponse({"Error": "No User matching query."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': Exception.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk=None):
        try:
            userprofile = UserProfile.objects.get(pk=pk)
            email = self.request.query_params.get('email', None)

            if email is not None:
                userprofile = UserProfile.objects.filter(user_id=request.user.id)

            serializer = UserProfileSerializer(userprofile, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        try:
            userprofile = UserProfile.objects.get(pk=pk)
            userprofile_user_id = userprofile.user_id
            user = User.objects.get(pk=userprofile_user_id)
            # email = self.request.query_params.get('email', None)
            print(request.data)

            if 'image' in request.data and request.data['image']:
                new_image = request.data['image']
                image = Image.objects.get(pk=new_image['id'])
                userprofile.image = image

            if 'is_currently_active' in request.data and request.data['is_currently_active']:
                is_currently_active = request.data['is_currently_active']
                userprofile.is_currently_active = is_currently_active

            if 'address' in request.data and request.data['address']:
                address = request.data['address']
                userprofile.address = address

            userprofile.user = user
            userprofile.save()
            return Response({'UserProfile Updated Successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            userprofile = UserProfile.objects.get(pk=pk)
            userprofile.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
