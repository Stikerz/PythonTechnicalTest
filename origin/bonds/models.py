from bonds.helpers.currencies import CURRENCY_LIST
from bonds.utils.services import get_lei_legalname
from django.contrib.auth.models import User
from django.db import models


class Bond(models.Model):

    CURRENCY_CHOICES = CURRENCY_LIST

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isin = models.CharField(unique=True, max_length=12)
    size = models.IntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    maturity = models.DateField()
    lei = models.CharField(max_length=20)
    legal_name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        payload = {"lei": self.lei}
        self.legal_name = get_lei_legalname(payload)
        super(Bond, self).save(*args, **kwargs)
