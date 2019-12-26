# -*- coding: utf-8 -*-
from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=200)
    urls_number = models.IntegerField(default=0)

    def __repr__(self):
        return 'Document ' + self.name


class Urls(models.Model):
    url = models.URLField()
    documents = models.ManyToManyField(Document, related_name='urls')
    alive = models.BooleanField(default=False)

    def __repr__(self):
        return self.url

    @property
    def get_num_docs(self):
        return self.documents_set.all().count()
