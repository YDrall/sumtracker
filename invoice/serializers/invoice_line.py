from rest_framework import serializers

from invoice.models import InvoiceLine


class InvoiceLineSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     pass

    id = serializers.IntegerField(required=False)

    class Meta:
        fields = ('product', 'quantity', 'price_without_tax',
                  'tax_name', 'tax_amount', 'line_total', 'invoice', 'id')
        model = InvoiceLine
