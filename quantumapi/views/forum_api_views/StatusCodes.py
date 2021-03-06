from rest_framework.authentication import authenticate, SessionAuthentication, BasicAuthentication, RemoteUserAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumforum.models import StatusCode as StatusCodeModel




class StatusCodeSerializer(serializers.ModelSerializer):
        class Meta:
            model = StatusCodeModel
            fields = ('id', 'code')
            depth = 1



class StatusCodes(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def list(self, request):
        all_status_codes = StatusCodeModel.objects.all()
        serializer = StatusCodeSerializer(all_status_codes, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            status_code = StatusCodeModel.objects.get(pk=pk)
            serializer = StatusCodeSerializer(status_code, context={'request': request})
            return Response(serializer.data)

        except StatusCodeModel.DoesNotExist as ex:
            return Response({'message': ex.args}, status=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            return Response({'message': exc.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request):
        try:
            code = request.data['code']
            data = {
                'code': code
            }
            serializer = StatusCodeSerializer(data=data, context={'request': request})
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({'Data Error': serializer.errors, "Exception": ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        pass


    def destroy(self, request, pk=None):
        pass
