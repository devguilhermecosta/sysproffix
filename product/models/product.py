from django.db import models
from stock.models import Stock


class ProductGroup(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)

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

    def __str__(self) -> str:
        return self.product.name
