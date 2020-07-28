from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import Messages
from django.contrib.auth.decorators import login_required



class MessagesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Messages
        url = serializers.HyperlinkedIdentityField(
            view_name='messages',
            lookup_field='id'
        )
        fields = ('id', 'url', 'message', 'timestamp', 'user_id', 'user', )
        depth = 2


class Message(ViewSet):
    def create(self, request):
        newmessage = Messages()
        newmessage.user_id = request.data["user_id"]
        newmessage.message = request.data["message"]
        newmessage.timestamp = request.data["timestamp"]

        newmessage.save()
        serializer = MessagesSerializer(newmessage, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            message = Messages.objects.get(pk=pk)
            serializer = MessagesSerializer(message, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        message = Messages.objects.get(pk=pk)
        message.user_id = request.data["user_id"]
        message.message = request.data["message"]
        message.timestamp = request.data["timestamp"]

        message.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            message = Messages.objects.get(pk=pk)
            message.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Messages.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        messages = Messages.objects.all()
        serializer = MessagesSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)
