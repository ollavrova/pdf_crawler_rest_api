"""pdf_rawler URL Configuration

"""
from django.conf.urls import url, include

from pdf_crawler.views import home, DocumentList, DocumentDetail, UrlsListView

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^documents/$',  DocumentList.as_view(), name='document-list'),
    url(r'^documents/(?P<pk>[0-9]+)/$', DocumentDetail.as_view(), name='document-detail'),
    url(r'^urls/$', UrlsListView.as_view(), name='url-list'),


]
