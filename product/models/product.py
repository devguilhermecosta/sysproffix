from django.db import models
from stock.models import Stock


class ProductGroup(models.Model):
    name = models.CharField(max_length=255,
                            blank=False,
                            null=False,
                            unique=True,
                            verbose_name='descrição',
                            error_messages={
                                'unique': 'já existe um grupo com este nome',
                            }
                            )

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    group = models.ForeignKey(ProductGroup,
                              on_delete=models.CASCADE,
                              verbose_name='grupo',
                              )
    code = models.CharField(max_length=255,
                            blank=False,
                            null=False,
                            unique=True,
                            verbose_name='código',
                            error_messages={
                                'unique': 'já existe um produto com este código'  # noqa: E501
                            }
                            )
    name = models.CharField(max_length=255,
                            blank=False,
                            null=False,
                            verbose_name='descrição',
                            )

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
