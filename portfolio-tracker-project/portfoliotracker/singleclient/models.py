from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
MAX_LENGTH = 50
MAX_DIGITS = 15
DECIMAL_PLACES = 5
ALPHANUMERIC = RegexValidator(
    r"^[0-9a-zA-Z_]*$", "Only alphanumeric characters are allowed."
)
ALPHABET = RegexValidator(r"[A-Za-z]*$", "Only alphabetic characters are allowed.")


class Advisor(models.Model):
    advisorid = models.CharField(validators=[ALPHANUMERIC], max_length=MAX_LENGTH)
    advisor = models.CharField(max_length=MAX_LENGTH)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.advisorid

    class Meta:
        unique_together = ["advisorid"]


class Client(models.Model):
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    clientid = models.CharField(max_length=MAX_LENGTH)
    name = models.CharField(max_length=MAX_LENGTH)

    CLIENT_TYPE_CHOICES = [
        ("INDIVIDUAL", "Individual"),
        ("CORPORATION", "Corporation"),
        ("TRUST", "Trust"),
        ("FOUNDATION", "Foundation"),
    ]

    client_type = models.CharField(
        choices=CLIENT_TYPE_CHOICES, max_length=MAX_LENGTH, default="INDIVIDUAL"
    )
    date_opened = models.DateField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.clientid} - {self.name}"

    class Meta:
        unique_together = ["clientid"]


class AccountType(models.Model):
    account_type = models.CharField(max_length=50, validators=[ALPHABET])

    def __str__(self):
        return self.account_type

    class Meta:
        unique_together = ["account_type"]


class Account(models.Model):
    accountid = models.CharField(max_length=MAX_LENGTH)
    clientid = models.ForeignKey(Client, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=MAX_LENGTH)
    date_opened = models.DateField()
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    inception_date = models.DateField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accountid} - {self.account_name}"

    class Meta:
        unique_together = ["accountid"]


class SecurityAssetClass(models.Model):
    security_asset_class = models.CharField(max_length=50, validators=[ALPHABET])

    def __str__(self):
        return self.security_asset_class

    class Meta:
        unique_together = ["security_asset_class"]
        verbose_name = "Security Asset Class"
        verbose_name_plural = "Security Asset Classes"


class Security(models.Model):
    securityid = models.CharField(max_length=MAX_LENGTH)
    isin = models.CharField(max_length=MAX_LENGTH, blank=True)
    ticker = models.CharField(max_length=MAX_LENGTH, blank=True)
    unit_of_measure = models.DecimalField(
        max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, null=True
    )
    name = models.CharField(max_length=MAX_LENGTH)
    asset_class = models.ForeignKey(SecurityAssetClass, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.securityid} - {self.name}"

    class Meta:
        unique_together = ["securityid"]
        verbose_name_plural = "Securities"


class SecurityPrice(models.Model):
    securityid = models.ForeignKey(Security, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.securityid} - {self.date} - {self.price}"

    class Meta:
        unique_together = ["securityid", "date"]


class Transaction(models.Model):
    accountid = models.ForeignKey(Account, on_delete=models.CASCADE)
    security = models.ForeignKey(Security, on_delete=models.CASCADE, blank=True)
    trade_date = models.DateField()

    TRANSACTION_TYPE_CHOICES = [
        ("BUY", "Buy"),
        ("SELL", "Sell"),
        ("DEPOSIT", "Deposit"),
        ("WITHDRAWAL", "Withdrawal"),
        ("INSTRUMENT-CASHFLOW", "instrument-cashflow"),
    ]
    trx_type = models.CharField(
        choices=TRANSACTION_TYPE_CHOICES, max_length=MAX_LENGTH, blank=False
    )
    trx_qty = models.DecimalField(
        max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, blank=True
    )
    trx_amt = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    trxid = models.CharField(max_length=MAX_LENGTH, validators=[ALPHANUMERIC])
    comment = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.trxid}"

    class Meta:
        unique_together = ["trxid"]


class Position(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    security = models.ForeignKey(Security, on_delete=models.CASCADE)
    date = models.DateField()
    mv = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, null=True)
    qty = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)

    def __str__(self) -> str:
        return f"Position - {self.account}|{self.security}|{self.date}"

    class Meta:
        unique_together = ["account", "security", "date"]
