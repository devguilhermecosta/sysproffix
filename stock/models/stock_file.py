from django.db import models


class StockFile(models.Model):
    doc = models.FileField(blank=True,
                           null=True,
                           default='',
                           upload_to='media/stock_movements/',
                           )

    def __str__(self) -> str:
        return self.doc.name
