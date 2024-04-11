from django.db import models


class Hospital(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False)
    state = models.CharField(max_length=2, null=False, blank=False)
