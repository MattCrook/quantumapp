from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import Messages
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from quantumapi.models import NewsArticle


class NewsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = NewsArticle
        url = serializers.HyperlinkedIdentityField(
            view_name='news',
            lookup_field='id'
        )
        fields = ('id', 'date', 'title', 'type', 'article', 'image')
        depth = 1


class News(ViewSet):
    def list(self, request):
        section = self.request.query_params.get('content', None)
        if section is not None:
            if section == 'all':
                content = NewsArticle.objects.all()
                serializer = NewsSerializer(content, many=True, context={'request': request})
                return Response(serializer.data)
            if section == 'corporate':
                content = NewsArticle.objects.filter(type=section)
                serializer = NewsSerializer(content, many=True, context={'request': request})
                return Response(serializer.data)
            if section == 'insights':
                content = NewsArticle.objects.filter(type=section)
                serializer = NewsSerializer(content, many=True, context={'request': request})
                return Response(serializer.data)
            if section == 'recent':
                content = NewsArticle.objects.filter(type=section)
                serializer = NewsSerializer(content, many=True, context={'request': request})
                return Response(serializer.data)
            if section == 'user_articles':
                content = NewsArticle.objects.filter(type=section)
                serializer = NewsSerializer(content, many=True, context={'request': request})
                return Response(serializer.data)
            else:
                print("OOPS 1")
        else:
            content = NewsArticle.objects.all()
            serializer = NewsSerializer(content, many=True, context={'request': request})
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if pk is not None:
            content = NewsArticle.objects.get(pk=pk)
            serializer = NewsSerializer(content, context={'request': request})
            return Response(serializer.data)





# @login_required
# @api_view(['GET', 'POST'])
# def news(request):
#     if request.method == 'GET':
#         section = request.query_params.get('content', None)
#         if section is not None:
#             if section == 'all':
#                 content = NewsArticle.objects.all()
#                 serializer = NewsSerializer(content, context={'request': request})
#                 return Response(serializer.data)
#             else:
#                 print("OOPS 1")
#         else:
#             print("OOPS 2")
