from django.db import models

class OpenInterest(models.Model):
    id=models.BigAutoField(primary_key=True)
    callOi=models.IntegerField()
    putOi=models.IntegerField()
    pcr=models.IntegerField()
    date=models.DateTimeField()
