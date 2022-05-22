from pandas import Series, DataFrame, concat, date_range


class Transaction:
    class DNATable:
        SECURITY = {
            "buy": 1,
            "sell": -1,
            "deposit": 0,
            "withdrawal": 0,
            "instrument-cashflow": 0,
        }

        CASH = {
            "buy": -1,
            "sell": 1,
            "deposit": 1,
            "withdrawal": -1,
            "instrument-cashflow": 1,
        }


class TrackingModel(Transaction):
    def __init__(self) -> None:
        """
        attributes are a strict reference to column headers as they appear in the db
        see singleclient.models. Any change to model names should result in a change
        to the attributes here.
        """
        self.dte = "trade_date"
        self.ttype = "trx_type"
        self.acct = "accountid"
        self.amt = "trx_amt"
        self.qty = "trx_qty"
        self.security = "security"

        # Model fields
        self.cash_ffect = "cash_effect"
        self.qty_ffect = "qty_effect"
        self.cash = "cash"
        self.order = "trxid"
        self.trx_order = [self.acct, self.dte, self.order]
        self.position = [self.acct, self.security, self.dte]

    def _order_trxs(self, trxs: DataFrame) -> DataFrame:
        """
        Relies on the following data types for the following params
        self.acct : str,
        self.dte : datetime,
        """
        return trxs.sort_values(by=self.trx_order)

    def _get_trx_direction(self, trxs: DataFrame, cash=True) -> Series:
        if cash:
            lookup = self.DNATable.CASH
        else:
            lookup = self.DNATable.SECURITY
        return trxs[self.ttype].map(lookup)

    def _get_trx_qty_ffect(self, trxs: DataFrame) -> Series:
        qty_direction = self._get_trx_direction(trxs, False)
        return qty_direction * trxs[self.qty].fillna(0)

    def _get_trx_cash_effect(self, trxs: DataFrame) -> Series:
        cash_direction = self._get_trx_direction(trxs)
        return cash_direction * trxs[self.amt].fillna(0)

    def get_position_qtys(self, df: DataFrame) -> DataFrame:
        _df = df[df[self.security] != "Cash"]
        grpd = _df.groupby(self.position)
        _res = grpd[self.qty_ffect].sum().cumsum()
        res = _res.reset_index()
        res.rename(columns={self.qty_ffect: "qty"}, inplace=True)
        return res

    def get_acct_cash(self, df: DataFrame) -> DataFrame:
        grpd = df.groupby([self.acct, self.dte])
        _res = grpd[self.cash_ffect].sum().cumsum()
        res = _res.reset_index()
        res.rename(columns={self.cash_ffect: "qty"}, inplace=True)
        return res

    def cleanup_positions(self, qty, cash):
        df = concat([qty, cash])
        df[self.security].fillna("Cash", inplace=True)
        df.rename(columns={self.dte: "date", self.security: "securityid"}, inplace=True)
        return df

    def _reindex_posn(self, df: DataFrame) -> DataFrame:
        """
        df is a single position timeseries
        """
        _df = df.sort_values(by='date').set_index('date')
        res = _df.resample('D').fillna(method='ffill')
        return res.reset_index()

    def _reindex_acct_posns(self, df: DataFrame) -> DataFrame:
        """
        df is account positions
        """
        instrs = set(df.securityid)
        psns = []
        for instr in instrs:
            _df = df[df.securityid == instr]
            re_psn = self._reindex_posn(_df)
            psns.append(re_psn)
        res = concat(psns)
        return res

    def reindex_posns_daily(self, df: DataFrame) -> DataFrame:
        """
        df is cleaned up, tracked, positions
        """
        accts = set(df[self.acct])
        posns = []
        for acct in accts:
            _df = df[df[self.acct]==acct]
            re_psn = self._reindex_acct_posns(_df)
            posns.append(re_psn)
        res = concat(posns)
        return res


    def track(self, trxs: DataFrame) -> DataFrame:
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
        qty = self.get_position_qtys(ord_trxs)
        cash = self.get_acct_cash(ord_trxs)
        _res = self.cleanup_positions(qty, cash)
        res = self.reindex_posns_daily(_res)
        return res
