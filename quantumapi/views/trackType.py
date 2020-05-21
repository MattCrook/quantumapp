from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import Tracktype


class TracktypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tracktype
        url = serializers.HyperlinkedIdentityField(
            view_name='tracktype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'rollercoasters')
        depth = 1


class Tracktypes(ViewSet):
    def create(self, request):
        newtracktype = Tracktype()
        newtracktype.name = request.data["name"]

        newtracktype.save()
        serializer = TracktypeSerializer(newtracktype, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            tracktype = Tracktype.objects.get(pk=pk)
            serializer = TracktypeSerializer(tracktype, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        tracktype = Tracktype.objects.get(pk=pk)

        tracktype.name = request.data["name"]
        tracktype.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            tracktype = Tracktype.objects.get(pk=pk)
            tracktype.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Tracktype.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        tracktypes = Tracktype.objects.all()
        serializer = TracktypeSerializer(tracktypes, many=True, context={'request': request})
        return Response(serializer.data)
