from django.db import models
from django.forms.widgets import ClearableFileInput
from django import forms
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import Image

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        image = serializers.ImageField(max_length=None, use_url=True)
        fields = ('id', 'image', )

    def create(self, validated_data):
        return Image.objects.create(**validated_data)



class Images(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    # def list(self, request):
    #     images = Image.objects.all()
    #     serializer = ImageSerializer(images, many=True, context={'request': request})
    #     return Response(serializer.data)


    # def create(self, request):
    #     new_image = Image()
    #     new_image.image = request.data["image"]
    #     new_image.save()
    #     serializer = ImageSerializer(new_image, context={'request': request})
    #     return Response(serializer.data)


    # def retreive(self, request, pk=None):
    #     try:
    #         image = Image.objects.get(pk=pk)
    #         serializer = ImageSerializer(image, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    # def update(self, request, pk=None):
    #     try:
    #         image = Image.objects.get(pk=pk)
    #         image.image = request.data["image"]
    #         image.save()
    #         serializer = ImageSerializer(image, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    # def destroy(self, request):
    #     pass
