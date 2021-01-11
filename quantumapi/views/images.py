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
        fields = ('id', 'image',)


    def create(self, validated_data):
        return Image.objects.create(**validated_data)


class Images(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


# def save_picture(form_picture):
#     """
#     Takes in MultiDict image form and coverts given image name of file to a hash.
#     Appends the hash to the file extenston then creates a path to the static/media directory
#     where it will be saved.
#     """
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/media', picture_fn)
#     i = Image.open(form_picture)
#     i.save(picture_path)
#     return picture_fn


# def save_picture_invoice_settings(form_picture):
#     """
#     Takes in MultiDict image form and coverts given image name of file to a hash.
#     Appends the hash to the file extenston then creates a path to the static/media/invoice_media directory
#     where it will be saved as the user's custom image for invoices.
#     """
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/media/invoice_media', picture_fn)
#     i = Image.open(form_picture)
#     i.save(picture_path)
#     return picture_fn
