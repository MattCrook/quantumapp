# from django.http import HttpResponseServerError
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import serializers
# from rest_framework import status
# from quantumapi.models import Credit, RollerCoaster, UserProfile


# class CreditsSerializer(serializers.HyperlinkedModelSerializer):

#     class Meta:
#         model = Credit
#         url = serializers.HyperlinkedIdentityField(
#             view_name='credit',
#             lookup_field='id'
#         )
#         fields = ('id', 'url', 'rollerCoaster', 'userProfile', )
#         depth = 1


# class Credits(ViewSet):

#     def retrieve(self, request, pk=None):
#         try:
#             credit = Credit.objects.get(pk=pk)
#             serializer = CreditsSerializer(credit, context={'request': request})
#             return Response(serializer.data)
#         except Exception as ex:
#             return HttpResponseServerError(ex)

#     def list(self, request):
#         userprofile = UserProfile.objects.get(user=request.auth.user)
#         user_credits = Credit.objects.filter(userprofile=userprofile)
#         # Not sure about this
#         # creditId = RollerCoaster.objects.get(request.data['creditId'])

#         serializer = CreditsSerializer(user_credits, many=True, context={'request': request})
#         return Response(serializer.data)

#     def create(self, request):

#         rollercoaster = RollerCoaster.objects.get(pk=request.data["rollerCoaster_id"])
#         userprofile = UserProfile.objects.get(user=request.auth.user)

#         new_credit = Credit()
#         new_credit.userprofile = userprofile
#         new_credit.rollercoaster = rollercoaster

#         new_credit.save()

#         serializer = CreditsSerializer(new_credit, context={'request': request})

#         return Response(serializer.data)

#     # def update(self, request, pk=None):
#     #     """Handle PUT requests for an individual itinerary item
#     #     Returns:
#     #         Response -- Empty body with 204 status code
#     #     """
#     #     itinerary = Itinerary.objects.get(pk=pk)
#     #     itinerary.starttime = request.data["starttime"]
#     #     attraction = Attraction.objects.get(pk=request.data["attraction_id"])
#     #     itinerary.attraction = attraction
#     #     itinerary.save()

#     #     return Response({}, status=status.HTTP_204_NO_CONTENT)

#     def destroy(self, request, pk=None):
#         try:
#             credit = Credit.objects.get(pk=pk)
#             credit.delete()

#             return Response({}, status=status.HTTP_204_NO_CONTENT)

#         except Credit.DoesNotExist as ex:
#             return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as ex:
#             return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
