# -*- coding: utf-8 -*-
import re
import requests
from django.shortcuts import render
from django.urls import reverse
from rest_framework.response import Response
from pdf_crawler.forms import UploadFileForm
from rest_framework import generics, status
from rest_framework.decorators import api_view
from pdf_crawler.models import Document, Urls
from pdf_crawler.serializers import DocumentSerializer, DocumentUrlsSerializer, UrlsListSerializer, UrlsDetailSerializer
from tika import parser


@api_view(['GET', 'POST'])
def home(request):
    form = UploadFileForm()
    message = ''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = {'pdf_file': open(request.FILES['pdf'].name, 'rb')}
            response = requests.post(request.build_absolute_uri(reverse('pdf_crawler:document-list')), files=files)
            if response.status_code == 201:
                message = 'Created: ' + str(response.json())
            else:
                message = 'Error: ' + str(response.json())
    return render(request, 'pdf_crawler/home.html', {'form': form, 'message': message})


class DocumentList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of users and upload/parse PDF file for creating a document.
    """
    model = Document
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def post(self, request, *args, **kwargs):
        """
        method for upload pdf file and creating a document and urls records
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        pdf = request.FILES['pdf_file']
        if pdf.size > 5000000:
            return Response({'too big pdf file size(more 5 Mb)'}, status=status.HTTP_400_BAD_REQUEST)
        raw = parser.from_file(pdf.name)
        raw = str(raw)
        safe_text = raw.encode('utf-8', errors='ignore')
        safe_text = str(safe_text).replace("\n", " ").replace("\\", " ")
        urls = re.findall("(?P<url>https?://[^\s]+)", safe_text)
        if urls:
            # create a document
            data = dict(name=pdf.name)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            document = serializer.save()
            # create urls and write to document
            urls_number = len(set(urls))
            for url in set(urls):
                # define alive field - check if url is live
                alive = requests.get(url)
                if alive.status_code >= 400:
                    alive = False
                else:
                    alive = True
                data = dict(url=url, alive=alive)
                serializer_url = UrlsDetailSerializer(data=data)
                serializer_url.is_valid(raise_exception=True)
                # check if url exists
                if Urls.objects.filter(url=url).exists():
                    url_found = Urls.objects.filter(url=url).first()
                    if url_found not in document.urls_set.all():
                        document.urls_set.add(url_found)
                else:
                    u = serializer_url.save()
                    document.urls_set.add(u)
            document.urls_number = urls_number
            document.save()

            headers = self.get_success_headers(serializer.data)
            return Response(DocumentUrlsSerializer(document).data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response({'Urls not found!'}, status=status.HTTP_404_NOT_FOUND)


class DocumentDetail(generics.RetrieveAPIView):
    """
    API endpoint that represents a single Document.
    """
    model = Document
    serializer_class = DocumentUrlsSerializer
    queryset = Document.objects.all()


class UrlsDetail(generics.RetrieveAPIView):
    """
    API endpoint that represents a single Urls.
    """
    model = Urls
    serializer_class = UrlsDetailSerializer
    queryset = Urls.objects.all()


class UrlsListView(generics.ListAPIView):
    """
    API endpoint that represents a list of urls.
    """
    model = Urls
    serializer_class = UrlsListSerializer
    queryset = Urls.objects.all()
