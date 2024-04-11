from django.db import models
from stock.models import Stock


class Hospital(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False)
    state = models.CharField(max_length=2, null=False, blank=False)
    stock = models.OneToOneField(
        Stock,
        on_delete=models.CASCADE,
        related_name="stock",
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs) -> None:
        if not self.stock:
            new_stock = Stock.objects.create(f"stock of {self.name}")
            self.stock = new_stock

        return super().save(*args, **kwargs)
