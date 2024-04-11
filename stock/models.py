from django.db import models
from typing import override


class Stockmanager(models.Manager):
    @override
    def create(self, name):
        stock = self.model(name=name)
        stock.save(using=self._db)
        return stock


class Stock(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    objects = Stockmanager()

    def __str__(self) -> str:
        return self.name
