from singleclient.models import *
from util import to_bool
from csv import DictReader


def advisor(row: dict) -> None:
    Advisor.objects.get_or_create(
        advisorid=row["advisorid"],
        advisor=row["advisor"],
        is_active=to_bool(row["is_active"]),
    )


def client(row: dict) -> None:
    adv = Advisor.objects.get(advisorid=row["advisorid"])
    Client.objects.get_or_create(
        advisor_id=adv.id,
        clientid=row["clientid"],
        name=row["name"],
        client_type=row["client_type"].upper(),
        date_opened=row["date_opened"],
        is_active=to_bool(row["active_status"]),
    )


def account(row: dict) -> None:
    cli = Client.objects.get(clientid=row["clientid"])
    acct_typ = AccountType.objects.get(account_type=row["account_type"])
    Account.objects.get_or_create(
        clientid_id=cli.id,
        accountid=row["accountid"],
        account_name=row["name"],
        date_opened=row["open_date"],
        account_type=acct_typ.id,
        inception_date=row["inception_date"],
        is_active=to_bool(row["active_status"]),
    )


def security(row: dict) -> None:
    asst_cls = SecurityAssetClass.objects.get(security_asset_class=row["asset_class"])
    Security.objects.get_or_create(
        securityid=row["securityid"],
        isin=row["isin"],
        ticker=row["ticker"],
        unit_of_measure=row["unit_of_measure"],
        name=row["name"],
        asset_class_id=asst_cls.id,
    )


def price(rows: DictReader) -> None:
    """
    Prices are bulk created since there can be quite alot of them
    """

    def create_px(row):
        security = Security.objects.get(securityid=row["securityid"])
        px = SecurityPrice(
            securityid_id=security.id, price=float(row["price"]), date=row["date"]
        )
        return px

    pxs = [create_px(row) for row in rows]
    SecurityPrice.objects.bulk_create(pxs)


def trx(row: dict) -> None:
    acct = Account.objects.get(accountid=row["accountid"])
    sec = Security.objects.get(securityid=row["securityid"])
    qty = row["trx_qty"]
    Transaction.objects.get_or_create(
        accountid_id=acct.id,
        security_id=sec.id,
        trade_date=row["trade_date"],
        trx_type=row["trx_type"].upper(),
        trx_qty=float(qty) if qty else 0.0,
        trx_amt=float(row["trx_amt"]),
        trxid=row["trx_id"],
        comment=row["comment"],
    )
