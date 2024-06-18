from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    rating = models.FloatField()
    image = models.ImageField(upload_to='images/', blank= True,  null= True)
    # pic = charfield

    def __str__(self):
        return self.name