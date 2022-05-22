import pandas as pd
from django.db.models.base import ModelBase

# https://pypi.org/project/django-pandas/
from django_pandas.io import read_frame
from singleclient.models import Transaction, SecurityPrice


def to_bool(val: str) -> bool:
    return True if val == "TRUE" else False


class QueryUtils:
    """
    Class to handle queryset manipulations
    """

    @staticmethod
    def get_model_data(model: ModelBase, **kwargs) -> pd.DataFrame:
        qs = model.objects.all()
        df = read_frame(qs)
        if "parse_dates" in kwargs.keys():
            dte_cols = kwargs["parse_dates"]
            for col in dte_cols:
                df[col] = pd.to_datetime(df[col])

        if "parse_nums" in kwargs.keys():
            num_cols = kwargs["parse_nums"]
            for col in num_cols:
                df[col] = df[col].astype(float)
        return df


class TrackingUtils(QueryUtils):
    def get_tracking_inputs(self):
        trxs = self.get_model_data(
            Transaction, parse_dates=["trade_date"], parse_nums=["trx_qty", "trx_amt"]
        )
        pxs = self.get_model_data(
            SecurityPrice, parse_dates=["date"], parse_nums=["price"]
        )
        return trxs, pxs

    def reindex_positions(psns: pd.DataFrame) -> pd.DataFrame:
        ts = psns.set_index('date')
        grpd = ts.groupby(['accountid','securityid'])
        res = grpd.resample('D').ffill().reset_index()
        return res
