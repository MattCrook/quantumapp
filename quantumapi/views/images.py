from django.db import models
from django.forms.widgets import ClearableFileInput
from django import forms
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import Image, ImageForm


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
