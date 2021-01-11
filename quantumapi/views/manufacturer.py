from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import Manufacturer, RollerCoaster
from urllib.parse import urlencode


class ManufacturerSerializer(serializers.HyperlinkedModelSerializer):

    name = serializers.CharField()
    origin_country = serializers.CharField()
    company_website = serializers.CharField()
    rollercoasters = serializers.PrimaryKeyRelatedField(queryset=RollerCoaster.objects.all(), many=True)

    class Meta:
        model = Manufacturer
        # url = serializers.HyperlinkedIdentityField(view_name='manufacturer', lookup_field='id')
        fields = ('id', 'name', 'origin_country', 'company_website', 'rollercoasters')
        depth = 1


class Manufacturers(ViewSet):
    def create(self, request):
        serializer = ManufacturerSerializer(data=request.data, context={'request': request})
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            manufacturer = Manufacturer.objects.get(pk=pk)
            name = self.request.query_params.get('name', None)
            if name is not None:
                manufacturer = Manufacturer.objects.filter(name=name)

            serializer = ManufacturerSerializer(manufacturer, context={'request': request})
            return Response(serializer.data)

        except Manufacturer.DoesNotExist as ex:
            return Response({'message': ex.args}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        manufacturer = Manufacturer.objects.get(pk=pk)

        manufacturer.name = request.data["name"]
        manufacturer.origin_country = request.data["origin_country"]
        manufacturer.company_website = request.data["company_website"]

        manufacturer.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            manufacturer = Manufacturer.objects.get(pk=pk)
            manufacturer.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Manufacturer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        manufacturers = Manufacturer.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            manufacturers = manufacturers.filter(name=name)

        serializer = ManufacturerSerializer(manufacturers, many=True, context={'request': request})
        return Response(serializer.data)
