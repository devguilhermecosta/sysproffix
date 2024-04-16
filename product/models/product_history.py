from django.db import models
from .product import ProductItem


PRODUCT_HISTORY_CHOICES = (
    ('entrada', 'entrada'),
    ('saída', 'saída'),
)


class ProductHistory(models.Model):
    product_item = models.ForeignKey(ProductItem,
                                     on_delete=models.CASCADE,
                                     related_name='product_history',
                                     )
    date = models.DateField(auto_now_add=True)
    moviment = models.CharField(max_length=255,
                                blank=False,
                                null=False,
                                choices=PRODUCT_HISTORY_CHOICES,
                                )
    quantity = models.IntegerField(default=1, blank=False, null=False)
