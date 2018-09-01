from rest_framework import serializers
from django.utils.timezone import datetime
from rest_framework.exceptions import ValidationError

from invoice.models import Invoice, InvoiceLine
from invoice.serializers.invoice_line import InvoiceLineSerializer


class InvoiceSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     pass

    invoice_lines = serializers.SerializerMethodField()
    invoice_number = serializers.IntegerField(required=False)
    date = serializers.DateTimeField(required=False)

    def get_invoice_lines(self, obj):
        if not obj:
            return obj
        invoice_lines = InvoiceLine.objects.filter(invoice=obj)
        return InvoiceLineSerializer(invoice_lines, many=True).data

    def validate(self, data):
        validated_data = data
        invoice_lines = data.get('invoice_lines', [])
        invoice_quantity = 0
        invoice_total_amount = 0
        for line in invoice_lines:
            if not line.get('quantity'):
                raise ValidationError('Line item quantity is required')
            if not line.get('line_total'):
                raise ValidationError('Line item total is required')
            invoice_quantity += line.get('quantity')
            invoice_total_amount += line.get('line_total')

        validated_data['date'] = datetime.now()
        validated_data['total_quantity'] = invoice_quantity
        validated_data['total_amount'] = invoice_total_amount
        validated_data['invoice_lines'] = invoice_lines
        return validated_data

    def create(self, validated_data):
        invoice_lines = validated_data.pop('invoice_lines', [])
        invoice_lines_instances = []
        for line in invoice_lines:
            invoice_line = InvoiceLine(**line)
            invoice_lines_instances.append(invoice_line)

        last_invoice = Invoice.objects.all().order_by('invoice_number').last()
        invoice_number = last_invoice.invoice_number + 1
        validated_data['invoice_number'] = invoice_number

        invoice = Invoice.objects.create(**validated_data)
        InvoiceLine.objects.bulk_create(invoice_lines_instances)
        return invoice

    class Meta:
        fields = ('customer', 'date', 'invoice_number',
                  'total_quantity', 'total_amount', 'total_tax', 'invoice_lines')
        model = Invoice
