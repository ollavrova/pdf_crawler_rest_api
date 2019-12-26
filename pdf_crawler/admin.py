# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Document, Urls

admin.site.register(Document)
admin.site.register(Urls)