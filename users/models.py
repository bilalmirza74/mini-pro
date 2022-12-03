from django.db import models

# Create your models here.

class CustomerCloudData(models.Model):
    custname = models.CharField(max_length=100)
    datatype = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    servicename = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    file = models.FileField(upload_to='files/')
    cdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
    class Meta:
        db_table='CustomerFiles'


class KNNSuggestionModel(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    servicename = models.CharField(max_length=100)
    knnsuggestions = models.CharField(max_length=100)
    distance = models.CharField(max_length=100)
    cdate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.id
    class Meta:
        db_table='KnnSuggestions'