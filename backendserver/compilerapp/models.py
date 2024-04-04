from django.db import models

# Create your models here.
class Code(models.Model):
    code=models.TextField()
    output=models.TextField()
    def __str__(self):
        return self.code