from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import RollerCoaster


class RollerCoasterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RollerCoaster
        url = serializers.HyperlinkedIdentityField(
            view_name='rollercoaster',
            lookup_field='id',
        )
        fields = ('id', 'url', 'name', 'tracktype', 'max_height', 'max_speed', 'manufacturer', 'park')
        depth = 1


class RollerCoasters(ViewSet):
    def create(self, request):
        newrollercoaster = RollerCoaster()
        newrollercoaster.name = request.data["name"]
        newrollercoaster.trackType = request.data["name"]
        newrollercoaster.max_height = request.data["max_height"]
        newrollercoaster.max_speed = request.data["max_speed"]
        newrollercoaster.manufacturer = request.data["manufacturer"]
        newrollercoaster.park = request.data["park"]



        newrollercoaster.save()
        serializer = RollerCoasterSerializer(newrollercoaster, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            rollercoaster = RollerCoaster.objects.get(pk=pk)
            serializer = RollerCoasterSerializer(rollercoaster, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        rollercoaster = RollerCoaster.objects.get(pk=pk)

        rollercoaster.name = request.data["name"]
        rollercoaster.trackType = request.data["name"]
        rollercoaster.max_height = request.data["max_height"]
        rollercoaster.max_speed = request.data["max_speed"]
        rollercoaster.manufacturer = request.data["manufacturer"]
        rollercoaster.park = request.data["park"]

        rollercoaster.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            rollercoaster = RollerCoaster.objects.get(pk=pk)
            rollercoaster.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except RollerCoaster.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        rollercoasters = RollerCoaster.objects.all()
        serializer = RollerCoasterSerializer(
            rollercoasters, many=True, context={'request': request})
        return Response(serializer.data)
