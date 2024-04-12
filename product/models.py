from django.db import models
from stock.models import Stock


class ProductGroup(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class ProductItem(models.Model):
    stock = models.ForeignKey(Stock,
                              on_delete=models.CASCADE,
                              related_name="stock_items",
                              )
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="product_item",
                                )
    lot = models.CharField(max_length=255, blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self) -> str:
        return self.product.name


class PendingProduct(models.Model):
    stock = models.ForeignKey(Stock,
                              on_delete=models.CASCADE,
                              related_name="stock_pendings",
                              )
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="pending",
                                )
    pending_quantity = models.IntegerField(default=1, blank=False, null=False)
    quantity_replenished = models.IntegerField(default=0, blank=False, null=False)  # noqa: E501

    def __str__(self) -> str:
        return self.product.name
