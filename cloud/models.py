from django.db import models

# Create your models here.
class CspRegisterModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(unique=True,max_length=100)
    email = models.CharField(unique=True,max_length=100)
    locality = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    cdate = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'CspUsers'
