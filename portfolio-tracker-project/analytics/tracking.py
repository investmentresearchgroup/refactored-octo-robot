from pandas import Series, DataFrame, concat

class Transaction:
    class DNATable:
        SECURITY = {
            'buy': 1,
            'sell': -1,
            'deposit': 0,
            'withdrawal': 0,
            'instrument-cashflow': 0
        }

        CASH = {
            'buy': -1,
            'sell': 1,
            'deposit': 1,
            'withdrawal': -1,
            'instrument-cashflow': 1
        }


class TrackingModel(Transaction):
    def __init__(self) -> None:
        self.dte = "trade_date"
        self.ttype = "trx_type"
        self.acct = "accountid"
        self.amt = "trx_amt"
        self.qty = "trx_qty"
        self.security = "securityid"

        # Model fields
        self.cash_ffect = "cash_effect"
        self.intrdy_cash = "intraday_cash"
        self.qty_ffect = "qty_effect"
        self.intrdy_qty = "intraday_qty"
        self.cash = "cash"
        self.order = "trx_id"
        self.trx_order = [self.acct, self.dte, self.order]
        self.position = [self.acct, self.security]

    def _order_trxs(self, trxs: DataFrame) -> DataFrame:
        """
        Relies on the following data types for the following params
        self.acct : str,
        self.dte : datetime,
        """
        return trxs.sort_values(by=self.trx_order)

    def _get_trx_direction(self, trxs: DataFrame, cash=True) -> Series:
        if cash:
            lookup =self.DNATable.CASH
        else:
            lookup = self.DNATable.SECURITY
        return trxs[self.ttype].map(lookup)

    def _get_trx_qty_ffect(self, trxs:DataFrame) -> Series:
        qty_direction = self._get_trx_direction(trxs, False)
        return qty_direction * trxs[self.qty].fillna(0)

    def _get_trx_cash_effect(self, trxs: DataFrame) -> Series:
        cash_direction = self._get_trx_direction(trxs)
        return cash_direction * trxs[self.amt].fillna(0)

    def get_intrday_qty(self, df: DataFrame) -> Series:
        grpd_trxs = df.groupby(self.position, as_index=False)
        res = grpd_trxs[self.qty_ffect].cumsum()
        return res

    def track_acct_cash(self, df:DataFrame) -> DataFrame:
        df[self.cash] = df[self.cash_ffect].cumsum()
        return df

    def track_cash(self, df: DataFrame) -> DataFrame:
        accts = set(df[self.acct])
        intrday_cash = []
        print(f"Processing intraday cash for {len(accts)} account(s)..")
        for acct in accts:
            acct_frame = df[df[self.acct] == acct]
            acct_cash = self.track_acct_cash(acct_frame)
            intrday_cash.append(acct_cash)
        res = concat(intrday_cash)
        return res



    def track(self, trxs: DataFrame, pxs: DataFrame) -> DataFrame:
        """Does a full tracking of all cash an non-cash positions.
        Most expensive calcs:
        1. trxs get ordered once
        2. loop is used to determine running balance per cash bucket
        3. tracked cash bkt frames are concatenated.
        4. transactions file is reordered naturally again. #TODO: Try to do this ONLY once. (More efficient)
        """
        trxs[self.cash_ffect] = self._get_trx_cash_effect(trxs)
        trxs[self.qty_ffect] = self._get_trx_qty_ffect(trxs)

        ord_trxs = self._order_trxs(trxs)
        ord_trxs[self.intrdy_qty] = self.get_intrday_qty(ord_trxs)
        res = self.track_cash(ord_trxs)
        return res



