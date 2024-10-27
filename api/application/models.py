from django.db import models

# Create your models here.
class AppId(models.Model):
    id = models.AutoField(primary_key=True)
    app_id = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=255)


    def __str__(self):
        return self.app_id