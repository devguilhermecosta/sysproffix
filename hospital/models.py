from django.db import models
from stock.models import Stock


class Hospital(models.Model):
    name = models.CharField(max_length=255,
                            unique=True,
                            null=False,
                            blank=True,
                            verbose_name='nome',
                            )
    city = models.CharField(max_length=255,
                            null=False,
                            blank=True,
                            verbose_name='cidade',
                            )
    state = models.CharField(max_length=2,
                             null=False,
                             blank=True,
                             verbose_name='estado',
                             )
    stock = models.OneToOneField(
        Stock,
        on_delete=models.CASCADE,
        related_name="stock",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.stock:
            new_stock = Stock.objects.create(f"stock of {self.name}")
            self.stock = new_stock

        return super().save(*args, **kwargs)
