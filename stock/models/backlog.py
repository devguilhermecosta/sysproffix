from django.db import models
from .stock import Stock
from product.models import PendingProduct


stockbacklog_choices = (
    ('pendente', 'pendente'),
    ('reposto parcial', 'reposto parcial'),
    ('finalizado', 'finalizado'),
    ('cancelado', 'cancelado'),
)


class StockBacklogOrder(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    state = models.CharField(max_length=255,
                             blank=False,
                             null=False,
                             choices=stockbacklog_choices,
                             )
    pacient = models.CharField(max_length=255, blank=False, null=False)
    date_surgery = models.DateField(blank=False, null=False)


class StockBacklogItem(models.Model):
    order = models.ForeignKey(StockBacklogOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(PendingProduct, on_delete=models.CASCADE)
    nfs = models.CharField(max_length=255, blank=False, null=False)
