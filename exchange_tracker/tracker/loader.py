from tracker.models import *


def create_countryindex(line):
    return CountryIndex.objects.get_or_create(
        name=line['index'])


def create_indexprice(line):
    index, created = create_countryindex(line)
    return IndexPrice.objects.get_or_create(
        name=index, date=['date'], value=float[line['value']])


def create_sector(line):
    index, created = create_countryindex(line)
    return Sector.objects.get_or_create(
        country_index=index,
        name=line['sector']
    )


def create_industry(line):
    index, index_created = create_countryindex(line)
    sector, sector_created = create_sector(line)
    return Industry.objects.get_or_create(
        name=line['industry'],
        country_index=index,
        sector=sector
    )


def create_ticker(line):
    index, index_created = create_countryindex(line)
    sector, sector_created = create_sector(line)
    industry, industry_created = create_industry(line)
    return Ticker.objects.get_or_create(
        name=line['ticker'],
        country_index=index,
        sector=sector,
        full_name=line['fullname'],
        industry=industry
    )


def create_tickerprice(line):
    ticker, created = create_ticker(line)
    return TickerPrice.objects.get_or_create(
        ticker=ticker,
        date=line['date'],
        volume=float(line['volume']),
        change=float(line['change']),
        price=float(line['price'])
    )


FIELDS = {
    'Country Index': {'method': create_countryindex, 'required_fields': ['index']},
    'Index Price': {'method': create_indexprice, 'required_fields': ['index', 'date', 'value']},
    'Sector': {'method': create_sector, 'required_fields': ['index', 'sector']},
    'Industry': {'method': create_industry, 'required_fields': ['index', 'sector', 'industry']},
    'Ticker': {'method': create_ticker, 'required_fields': ['index', 'sector', 'industry', 'fullname', 'ticker']},
    'Ticker Price': {'method': create_tickerprice, 'required_fields': ['ticker', 'date', 'volume', 'change', 'price',
                                                                       'industry', 'sector', 'fullname', 'index']}
}
