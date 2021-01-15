from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import Tracktype, RollerCoaster
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class TracktypeSerializer(serializers.HyperlinkedModelSerializer):

    name = serializers.CharField()
    rollercoasters = serializers.PrimaryKeyRelatedField(queryset=RollerCoaster.objects.all(), many=True)
    class Meta:
        model = Tracktype
        # url = serializers.HyperlinkedIdentityField(view_name='tracktype', lookup_field='id')
        fields = ('id', 'name', 'rollercoasters')
        depth = 1


class Tracktypes(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def list(self, request):
        tracktypes = Tracktype.objects.all()
        name = self.request.query_params.get('name', None)

        if name is not None:
            tracktypes = Tracktype.objects.filter(name=name)

        serializer = TracktypeSerializer(tracktypes, many=True, context={'request': request})
        return Response(serializer.data)


    def create(self, request):
        serializer = TracktypeSerializer(data=request.data, context={'request': request})
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            tracktype = Tracktype.objects.get(pk=pk)
            serializer = TracktypeSerializer(tracktype, context={'request': request})
            return Response(serializer.data)

        except Tracktype.DoesNotExist as ex:
            return Response({'message': ex.args}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
