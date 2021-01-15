from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import Messages
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from quantumapi.models import NewsArticle
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

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
                Response({"Error": f'Section {section} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            content = NewsArticle.objects.all()
            serializer = NewsSerializer(content, many=True, context={'request': request})
            return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            if pk is not None:
                content = NewsArticle.objects.get(pk=pk)
                serializer = NewsSerializer(content, context={'request': request})
                return Response(serializer.data)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        new_news_article = NewsArticle()

        new_news_article.title = request.data["title"]
        new_news_article.type = request.data["type"]
        new_news_article.article = request.data["article"]
        new_news_article.image = request.data["image"]
        new_news_article.date = request.data["date"]

        new_news_article.save()
        serializer = NewsSerializer(new_news_article, context={'request': request})
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        try:
            news_article = NewsArticle.objects.get(pk=pk)
            news_article.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except news_article.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
