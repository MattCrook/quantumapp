from django.http import HttpResponseServerError, JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import RollerCoaster, Manufacturer, Tracktype, Park
from quantumapi.views.park import ParkSerializer
from quantumapi.views.manufacturer import ManufacturerSerializer
from quantumapi.views.trackType import TracktypeSerializer
import json
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication





class RollerCoasterSerializer(serializers.ModelSerializer):

    name = serializers.CharField()
    max_height = serializers.CharField()
    max_speed = serializers.CharField()
    # tracktype = TracktypeSerializer()
    # manufacturer = ManufacturerSerializer()
    # park = ParkSerializer()
    tracktype = serializers.PrimaryKeyRelatedField(queryset=Tracktype.objects.all())
    manufacturer = serializers.PrimaryKeyRelatedField(queryset=Manufacturer.objects.all())
    park = serializers.PrimaryKeyRelatedField(queryset=Park.objects.all())
    class Meta:
        model = RollerCoaster
        fields = ['id', 'name', 'tracktype', 'max_height', 'max_speed', 'manufacturer', 'park']
        depth = 1


class RollerCoasters(ViewSet):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def list(self, request):
        rollercoasters = RollerCoaster.objects.all()
        park_id = self.request.query_params.get("park_id", None);

        if park_id is not None:
            rollercoasters = rollercoasters.filter(park_id=park_id)
        serializer = RollerCoasterSerializer(rollercoasters, many=True, context={'request': request})
        return Response(serializer.data)


    def create(self, request):
        try:
            if 'isBulk' in request.data and request.data['isBulk']:
                incoming_queryset = request.data['data']
                all_serialized_data = []
                for new_entry in incoming_queryset:

                    manufacturer = Manufacturer.objects.get(pk=new_entry["manufacturerId"])
                    tracktype = Tracktype.objects.get(pk=new_entry["trackTypeId"])
                    park = Park.objects.get(pk=new_entry["parkId"])


                    # data = {
                    # 'name': new_entry["name"],
                    # 'tracktype': model_to_dict(tracktype),
                    # 'max_height': new_entry["max_height"],
                    # 'max_speed': new_entry["max_speed"],
                    # 'manufacturer': model_to_dict(manufacturer),
                    # 'park': model_to_dict(park),
                    # }


                    data = {
                    'name': new_entry["name"],
                    'tracktype': tracktype.pk,
                    'max_height': new_entry["max_height"],
                    'max_speed': new_entry["max_speed"],
                    'manufacturer': manufacturer.pk,
                    'park': park.pk,
                    }

                    try:
                        serialized_data = RollerCoasterSerializer(data=data, context={'request': request})
                        serialized_data.is_valid()
                        serialized_data.save()
                    except:
                        return Response({'Data Error': serialized_data.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    new_roller_coaster = {
                        'id': serialized_data.data['id'],
                        'name': serialized_data.data["name"],
                        'tracktype': serialized_data.data["tracktype"],
                        'max_height': serialized_data.data["max_height"],
                        'max_speed': serialized_data.data["max_speed"],
                        'manufacturer': serialized_data.data["manufacturer"],
                        'park': serialized_data.data["park"]
                    }

                    all_serialized_data.append(new_roller_coaster)

                response = {
                    "isBulk": True,
                    "serialized_data": all_serialized_data,
                }

                return Response(response)

        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            try:
                manufacturer = Manufacturer.objects.get(pk=request.data["manufacturerId"])
                tracktype = Tracktype.objects.get(pk=request.data["trackTypeId"])
                park = Park.objects.get(pk=request.data["parkId"])

                data = {
                'name': request.data["name"],
                'tracktype': tracktype.pk,
                'max_height': request.data["max_height"],
                'max_speed': request.data["max_speed"],
                'manufacturer': manufacturer.pk,
                'park': park.pk,
                }
                serializer = RollerCoasterSerializer(data=data, context={'request': request})
                serializer.is_valid()
                serializer.save()


                return Response(serializer.data)

            except Exception as ex:
                return Response({'Data Error': serializer.errors, "Exception": ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            rollercoaster = RollerCoaster.objects.get(pk=pk)
            serializer = RollerCoasterSerializer(rollercoaster, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def destroy(self, request, pk=None):
        try:
            rollercoaster = RollerCoaster.objects.get(pk=pk)
            rollercoaster.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except RollerCoaster.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
