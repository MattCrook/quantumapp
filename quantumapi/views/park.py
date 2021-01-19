from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import Park, RollerCoaster
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class ParkSerializer(serializers.HyperlinkedModelSerializer):

    name = serializers.CharField()
    parkCountry = serializers.CharField()
    parkLocation = serializers.CharField()
    rollercoasters = serializers.PrimaryKeyRelatedField(queryset=RollerCoaster.objects.all(), many=True)
    class Meta:
        model = Park
        fields = ('id', 'name', 'parkCountry', 'parkLocation', 'rollercoasters')
        depth = 1


class Parks(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]

    def list(self, request):
        parks = Park.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            parks = parks.filter(name=name)
        serializer = ParkSerializer(parks, many=True, context={'request': request})
        return Response(serializer.data)


    def create(self, request):
        serializer = ParkSerializer(data=request.data, context={'request': request})
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            park = Park.objects.get(pk=pk)
            serializer = ParkSerializer(park, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def update(self, request, pk=None):
        park = Park.objects.get(pk=pk)
        park.name = request.data["name"]
        park.parkLocation = request.data["parkLocation"]
        park.parkCountry = request.data["parkCountry"]
        park.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        try:
            park = Park.objects.get(pk=pk)
            park.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Park.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
