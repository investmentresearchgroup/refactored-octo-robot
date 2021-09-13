from django.db import models

# Create your models here.


class CountryIndex(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name']
        verbose_name = 'Country Index'
        verbose_name_plural = 'Country Indices'


class IndexPrice(models.Model):
    name = models.ForeignKey(CountryIndex, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=15, decimal_places=5)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = ['name', 'date']
        verbose_name_plural = 'Country Index Prices'


class Sector(models.Model):
    country_index = models.ForeignKey(CountryIndex, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = ['country_index', 'name']


class Industry(models.Model):
    country_index = models.ForeignKey(CountryIndex, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = ['country_index', 'sector', 'name']
        verbose_name_plural = 'Industries'


class Ticker(models.Model):
    country_index = models.ForeignKey(CountryIndex, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    full_name = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = ['country_index', 'sector', 'industry', 'name']


class TickerPrice(models.Model):
    models.ForeignKey(Ticker, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    volume = models.DecimalField(max_digits=15, decimal_places=5, default=0.0)
    change = models.DecimalField(max_digits=15, decimal_places=5, default=0.0)
    price = models.DecimalField(max_digits=15, decimal_places=5, default=0.0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticker} on {self.date}"

    class Meta:
        unique_together = ['ticker', 'date']
