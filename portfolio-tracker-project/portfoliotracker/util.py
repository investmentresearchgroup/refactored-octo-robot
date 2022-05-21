import pandas as pd
from django.db.models.base import ModelBase


def to_bool(val: str) -> bool:
    return True if val == "TRUE" else False


class ModelUtils:
    """
    Class to handle queryset manipulations
    """

    @staticmethod
    def queryset_to_df(model: ModelBase) -> pd.DataFrame:
        data = model.objects.values()
        df = pd.DataFrame.from_records(data)
        return df


class TrackingUtils:
    ...
