from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from invoice.models import Invoice, InvoiceLine
from invoice.serializers.invoice import InvoiceSerializer


class InvoiceListView(generics.ListCreateAPIView):

    # permission_classes = permissions.IsAuthenticated

    serializer_class = InvoiceSerializer

    queryset = Invoice.objects.all()

    # def post(self, request, *args, **kwargs):
    #     invoice_lines = request.POST.data.get('invoice_lines')
    #     invoice_lines_instances = []
    #     invoice_quantity = 0
    #     invoice_total_amount = 0
    #     for line in invoice_lines:
    #         if not line.get('quantity'):
    #             raise ValidationError('Line item quantity is required')
    #         if not line.get('line_total'):
    #             raise ValidationError('Line item total is required')
    #         invoice_quantity += line.get('quantity')
    #         invoice_total_amount += line.get('line_total')
    #         invoice_line, created = InvoiceLine(**line)
    #         invoice_lines_instances.append(invoice_line)
    #
    #     last_invoice = Invoice.objects.all().order_by('invoice_number').last()
    #     invoice_number = last_invoice.invoice_number + 1
    #     # validated_data['invoice_number'] = invoice_number
    #     # validated_data['date'] = datetime.now()
    #     # validated_data['total_quantity'] = invoice_quantity
    #     # validated_data['total_amount'] = invoice_total_amount
    #
    #     invoice = Invoice.objects.create(**validated_data)
    #     InvoiceLine.objects.bulk_create(invoice_lines_instances)
    #     return invoice



class InvoiceView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()

    def put(self, request, *args, **kwargs):
        pass
