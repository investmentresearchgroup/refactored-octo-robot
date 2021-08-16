from django.db import models

# Create your models here.

class Continent(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Contrie(models.Model):
    continent = models.ForeignKey(Continent,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class Ticker(models.Model):
    continent = models.ForeignKey(Continent,on_delete=models.CASCADE)
    country = models.ForeignKey(Contrie,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    long_name = models.CharField(max_length=200, blank=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.name}) - ({self.long_name})"


class Price(models.Model):
    continent = models.ForeignKey(Continent,on_delete=models.CASCADE)
    country = models.ForeignKey(Contrie,on_delete=models.CASCADE)
    ticker = models.ForeignKey(Ticker,on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10,decimal_places=5)
    date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticker},{self.value},{self.date}"


    class Meta:
        unique_together = ['continent','country','ticker','date']
