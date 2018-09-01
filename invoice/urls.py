# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .apis import (
    invoice
)

urlpatterns = [
    url(
        r'^$',
        invoice.InvoiceListView.as_view(),
        name='api_invoice_list'),

    url(
        r'^(?P<pk>[0-9]+)/$',
        invoice.InvoiceView.as_view(),
        name='api_invoice_crud'),
]
