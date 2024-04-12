from django.db import models
from transport.models import Transport
from .stock import Stock
from .stock_file import StockFile
from product.models import ProductItem


class StockReplenishmentOrder(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    nfs = models.CharField(max_length=255, blank=True, null=True)
    send_date = models.DateField(blank=False, null=False)
    receipt_date = models.DateField(blank=True, null=True)
    transport = models.ForeignKey(Transport, on_delete=models.DO_NOTHING)
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)


class StockReplenishmentItem(models.Model):
    order = models.ForeignKey(StockReplenishmentOrder, on_delete=models.CASCADE)  # noqa: E501
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)


class StockReplenishmentDoc(models.Model):
    order = models.ForeignKey(StockReplenishmentOrder, on_delete=models.CASCADE)  # noqa: E501
    file = models.ForeignKey(StockFile, on_delete=models.CASCADE)
