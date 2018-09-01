from django.utils.datetime_safe import datetime
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from invoice.models import Invoice, InvoiceLine
from invoice.serializers.invoice import InvoiceSerializer


class InvoiceListView(generics.ListCreateAPIView):

    serializer_class = InvoiceSerializer

    queryset = Invoice.objects.all()

    def perform_create(self, serializer):
        data = self.request.data
        validated_data = data
        invoice_lines = data.get('invoice_lines', [])
        invoice_quantity = 0
        invoice_total_amount = 0
        invoice_total_tax = 0
        for line in invoice_lines:
            if not line.get('quantity'):
                raise ValidationError('Line item quantity is required')
            if not line.get('line_total'):
                raise ValidationError('Line item total is required')
            invoice_quantity += float(line.get('quantity'))
            invoice_total_amount += float(line.get('line_total'))
            invoice_total_tax += float(line.get('tax_amount'))

        validated_data['date'] = datetime.now()
        validated_data['total_quantity'] = invoice_quantity
        validated_data['total_amount'] = invoice_total_amount
        validated_data['total_tax'] = invoice_total_tax
        validated_data['invoice_lines'] = invoice_lines
        last_invoice = Invoice.objects.all().order_by('invoice_number').last()
        invoice_number = last_invoice.invoice_number + 1
        validated_data['invoice_number'] = invoice_number
        serializer.save(**validated_data)


class InvoiceView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()

    def perform_update(self, serializer):
        data = self.request.data
        validated_data = data
        invoice_lines = data.get('invoice_lines', [])
        invoice_quantity = 0
        invoice_total_amount = 0
        invoice_total_tax = 0
        for line in invoice_lines:
            if not line.get('quantity'):
                raise ValidationError('Line item quantity is required')
            if not line.get('line_total'):
                raise ValidationError('Line item total is required')
            invoice_quantity += float(line.get('quantity'))
            invoice_total_amount += float(line.get('line_total'))
            invoice_total_tax += float(line.get('tax_amount'))

        validated_data['date'] = datetime.now()
        validated_data['total_quantity'] = invoice_quantity
        validated_data['total_amount'] = invoice_total_amount
        validated_data['total_tax'] = invoice_total_tax
        validated_data['invoice_lines'] = invoice_lines
        print(self.kwargs.get('pk'))
        invoice = Invoice.objects.get(id=self.kwargs.get('pk'))
        serializer.update(invoice, validated_data)