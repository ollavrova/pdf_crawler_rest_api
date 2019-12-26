from pdf_crawler.models import Document, Urls
from rest_framework import serializers


# Serializers define the API representation.
class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ['id', 'name', 'urls_number']


class UrlsDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Urls
        fields = ['id', 'url', 'alive', ]


class UrlsListSerializer(serializers.ModelSerializer):
    num_docs = serializers.SerializerMethodField()

    class Meta:
        model = Urls
        fields = ['id', 'url', 'alive', 'num_docs', ]

    def get_num_docs(self, obj):
        return obj.documents.all().count()


class DocumentUrlsSerializer(serializers.HyperlinkedModelSerializer):
    urls = UrlsDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'name', 'urls', ]

