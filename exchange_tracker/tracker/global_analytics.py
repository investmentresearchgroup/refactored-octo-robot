# Library to store all quantitative methods,etc

from typing import Dict,Tuple,TypeVar
import pandas as pd
import numpy as np
import warnings
from datetime import timedelta

PandasDataFrame = TypeVar('pd.core.frame.DataFrame')
PandasDateTimeObject = TypeVar('pd.core.indexes.datetimes.DatetimeIndex')

class SeriesUtilities:

    def __sanitize_series(self,series: PandasDataFrame) -> PandasDataFrame:
        '''Used to remove duplicate date indices...until we get cleaner data'''
        if self.__series_has_duplicate_dates(series):
            return series.loc[~series.index.duplicated(keep='first'), ]
        else:
            return series

    @staticmethod
    def __series_has_duplicate_dates(series: PandasDataFrame) -> bool:
        check = any(series.index.duplicated(keep=False))
        return check

    def get_nearest_date_in_series(self, series: PandasDataFrame,
                                   dt: PandasDateTimeObject) -> PandasDataFrame:
        sanitized_series = self.__sanitize_series(series)
        idx = sanitized_series.index.get_loc(dt, method='nearest')
        return sanitized_series.index[idx]

    def get_series_current_value(self,series:PandasDataFrame)-> float:
        sanitized_series = self.__sanitize_series(series)
        latest_date = sanitized_series.index.max()
        return sanitized_series.loc[latest_date,].values[0]

    def get_series_begining_of_year_value(self,series:PandasDataFrame) -> float:
        sanitized_series = self.__sanitize_series(series)
        latest_date = sanitized_series.index.max()
        year_start = pd.to_datetime(f"{latest_date.year}-01-01")
        idx = sanitized_series.index.get_loc(year_start, method='nearest')
        data_yr_start = sanitized_series.index[idx]
        return sanitized_series.loc[data_yr_start,].values[0]

    def get_series_previous_dt_value(self,series:PandasDataFrame) -> float:
        sanitized_series = self.__sanitize_series(series)
        previous_date = sanitized_series.index.max() - pd.DateOffset(1)
        idx = sanitized_series.index.get_loc(previous_date, method='ffill')
        data_prev_date = sanitized_series.index[idx]
        return sanitized_series.loc[data_prev_date,].values[0]

    def get_series_log_return(self,series:PandasDataFrame) -> PandasDataFrame:
        clean_series = self.__sanitize_series(series)
        sorted_series = clean_series.sort_index()
        log_return = np.log(sorted_series/sorted_series.shift(-1))
        return log_return



class AnalyticsLib(SeriesUtilities):
    def __init__(self):
        self.__period_strings = ['1 Month', '3 Month', '6 month', '1 year', '3 year', '5 year', '10 year']
        self.__period_days = [30, 90, 180, 365, 1095, 1825, 3650]
        self.__period_dict = dict(zip(self.__period_strings,self.__period_days))

    @staticmethod
    def calculate_return(val1: float, val2: float) -> float:
        if val1 == 0:
            warnings.warn(
                f"Returns are being calculated for at least one zero value: {val1},{val2}"
            )
            return 0
        elif (pd.isna(val1)) or (pd.isna(val2)):
            warnings.warn(
                f"You have at least one missing input: {val1},{val2}"
            )
            return 0
        assert isinstance(val1, float), 'First input must be a float'
        assert isinstance(val2, float), 'Second input must be a float'
        return val2 / val1 - 1

    @staticmethod
    def calculate_pct_change(val1:float,val2:float) -> float:
        if val2 == 0:
            return -1
        return val1/val2 - 1

    def calc_annualized_vol(self,series:PandasDataFrame) -> float: #TODO: State the assumptions here friend
        log_return = self.get_series_log_return(series)
        daily_std = np.std(log_return) #TODO: Assumption is that data is daily
        #TODO: spec for annualized std: ann_std = daily_std * 252 ** 0.5
        daily_vol = daily_std**2
        return daily_vol.values[0]

    def __generate_return_periods(self, start: PandasDateTimeObject,
                                  end: PandasDateTimeObject) -> Dict[str,int]:
        days_between: int = (end - start).days
        series_has_return_days = lambda period_pair: period_pair[1] <= days_between
        selected_period_pairs: Dict = dict(filter(series_has_return_days, self.__period_dict.items()))
        selected_period_pairs['Since Inception'] = days_between
        return selected_period_pairs

    # TODO Add validation here before making public or static
    def __single_period_return(self, series: PandasDataFrame,
                               period_days: int, period_end: PandasDateTimeObject) -> float:
        period_start = period_end - timedelta(period_days)
        chosen_start = self.get_nearest_date_in_series(series, period_start)
        start_val, end_val = series.loc[chosen_start][0], series.loc[period_end][0]
        return self.calculate_return(start_val, end_val)


    def calculate_periodic_returns(self, series: PandasDataFrame,scale=100) -> Dict[str,float]:
        assert isinstance(series.index, pd.core.indexes.datetimes.DatetimeIndex), \
            "Series input must have a datetime index. Convert using pd.to_datetime"
        start, end = series.index.min(), series.index.max()
        period_pairs = self.__generate_return_periods(start,end)
        periodic_returns = {period_str:self.__single_period_return(
            series,period_days,end) *scale for (period_str,period_days) in period_pairs.items()}
        return periodic_returns

    def get_series_period_volatility(self,period_start_date:PandasDateTimeObject,series:PandasDataFrame)-> float:
        calc_series = series.loc[series.index >= period_start_date,]
        return self.calc_annualized_vol(calc_series)

    def series_summary(self,series:PandasDataFrame) -> Dict[str,str]:
        current_value = self.get_series_current_value(series)
        previous_value = self.get_series_previous_dt_value(series)
        beginning_of_yr_value = self.get_series_begining_of_year_value(series)
        current_return = self.calculate_return(previous_value,current_value)

        start, end = series.index.min(), series.index.max()
        year_start = pd.to_datetime(f"{end.year}-01-01")
        ytd_days = (end - year_start).days
        ytd_change = self.calculate_pct_change(current_value,beginning_of_yr_value)
        ytd_return = self.__single_period_return(series,ytd_days,end)
        ytd_vol = self.get_series_period_volatility(year_start,series)
        summary = {
            'Current Market Value':f"₵{current_value}",
            'Beginning of Year Market Value':f"₵{beginning_of_yr_value}",
            'Return (Current)':f"{current_return:.2%}",
            '% Change (YtD)':f"{ytd_change:.2%}",
            'Return (YtD)':f"{ytd_return:.2%}",
            'Volatility(YtD)':f"{ytd_vol:.2%}"
        }
        return summary

    def series_current_summary(self,series:PandasDataFrame) -> Tuple[float,float]: #TODO: Add more if needed
        current_value = self.get_series_current_value(series)
        previous_dt_value = self.get_series_previous_dt_value(series)
        current_return = self.calculate_return(previous_dt_value,current_value)
        return current_value,current_return