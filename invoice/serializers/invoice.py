from rest_framework import serializers

from invoice.models import Invoice, InvoiceLine
from invoice.serializers.invoice_line import InvoiceLineSerializer


class InvoiceSerializer(serializers.ModelSerializer):

    invoice_lines = serializers.SerializerMethodField(required=False)
    invoice_number = serializers.IntegerField(required=False)
    date = serializers.DateTimeField(required=False)
    total_quantity = serializers.DecimalField(required=False, decimal_places=2, max_digits=20)
    total_amount = serializers.DecimalField(required=False, decimal_places=2, max_digits=20)
    total_tax = serializers.DecimalField(required=False, decimal_places=2, max_digits=20)

    def get_invoice_lines(self, obj):
        if not obj:
            return obj
        invoice_lines = InvoiceLine.objects.filter(invoice=obj)
        return InvoiceLineSerializer(invoice_lines, many=True).data

    def create(self, validated_data):
        invoice_lines = validated_data.pop('invoice_lines', [])
        invoice_lines_instances = []
        invoice = Invoice.objects.create(**validated_data)
        for line in invoice_lines:
            invoice_line = InvoiceLine(**line)
            invoice_line.invoice = invoice
            invoice_lines_instances.append(invoice_line)

        InvoiceLine.objects.bulk_create(invoice_lines_instances)
        return invoice

    def update(self, instance, validated_data):
        existing_lines = list(InvoiceLine.objects.filter(invoice=instance))
        invoice_lines = validated_data.pop('invoice_lines', [])
        for line in invoice_lines:
            line['invoice_id'] = line.pop('invoice')
            if line.get('id'):
                line_instance = InvoiceLine.objects.get(id=line.pop('id'))
                line_instance.product = line.get('product')
                line_instance.quantity = line.get('quantity')
                line_instance.price_without_tax = line.get('price_without_tax')
                line_instance.tax_name = line.get('tax_name')
                line_instance.tax_amount = line.get('tax_amount')
                line_instance.line_total = line.get('line_total')
                line_instance.save()
                continue
            line_instance = InvoiceLine.objects.create(**line)

        # TODO: delete all invoice which are not in data but exists

        instance.customer = validated_data.get('customer')
        instance.total_quantity = validated_data.get('total_quantity')
        instance.total_amount = validated_data.get('total_amount')
        instance.total_tax = validated_data.get('total_tax')
        instance.save()

        return instance

    class Meta:
        fields = ('customer', 'date', 'invoice_number',
                  'total_quantity', 'total_amount', 'total_tax', 'invoice_lines')
        model = Invoice

