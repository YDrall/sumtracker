from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Invoice(models.Model):
    customer = models.CharField(
        max_length=256  # max length not mentioned in requirement so for now assuming it 256
    )
    date = models.DateTimeField(
        _('Invoice Date')
    )
    invoice_number = models.IntegerField()
    total_quantity = models.DecimalField(
        decimal_places=2,
        max_digits=20
    )
    total_amount = models.DecimalField(
        decimal_places=2,
        max_digits=20
    )
    total_tax = models.DecimalField(
        decimal_places=2,
        max_digits=20
    )

    def __str__(self):
        return str(self.invoice_number)

    def __unicode__(self):
        return str(self.invoice_number)


class InvoiceLine(models.Model):
    product = models.CharField(
        max_length=256  # max length not mentioned in requirement so for now assuming it 256
    )
    quantity = models.DecimalField(
        decimal_places=2,
        max_digits=20
    )
    price_without_tax = models.DecimalField(
        decimal_places=2,
        max_digits=20
    )
    tax_name = models.CharField(
        max_length=256  # max length not mentioned in requirement so for now assuming it 256
    )
    tax_amount = models.DecimalField(
        decimal_places=2,
        max_digits=20
    )
    line_total = models.DecimalField(
        decimal_places=2,
        max_digits=20
    )
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE  # all invoice lines must be deleted on deletion of an invoice
    )

    def __str__(self):
        return self.product

    def __unicode__(self):
        return self.product

