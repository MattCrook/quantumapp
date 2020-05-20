from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import Park


class ParkSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Park
        url = serializers.HyperlinkedIdentityField(
            view_name='park',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'parkCountry', 'parkLocation')


class Parks(ViewSet):
    def create(self, request):
        newpark = Park()
        newpark.name = request.data["name"]
        newpark.parkLocation = request.data["parkLocation"]
        newpark.parkCountry = request.data["parkCountry"]
        newpark.save()
        serializer = ParkSerializer(newpark, context={'request': request})
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

    def list(self, request):
        parks = Park.objects.all()
        serializer = ParkSerializer(
            parks, many=True, context={'request': request})
        return Response(serializer.data)
