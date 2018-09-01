from rest_framework import serializers

from invoice.models import InvoiceLine


class InvoiceLineSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     pass

    class Meta:
        fields = ('product', 'quantity', 'price_without_tax',
                  'tax_name', 'tax_amount', 'line_total', 'invoice')
        model = InvoiceLine
