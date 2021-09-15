import pandas as pd
import os
from global_analytics import AnalyticsLib
import requests

analib = AnalyticsLib()


def stock_price_data():
    price_file = os.path.join('data', 'gse_historical_data_v2.csv')
    stock_price_df = pd.read_csv(price_file, parse_dates=['Date'], usecols=[
                                 0, 1, 2, 3, 4])  # TODO: not recommended
    stock_price_df['price'] = pd.to_numeric(
        stock_price_df['price'], errors='coerce')
    stock_price_df['Year'] = stock_price_df['Date'].dt.year
    return stock_price_df.dropna(subset=['name'])


def gse_index_data():
    file = os.path.join('data', 'gse_ci_data.csv')
    df = pd.read_csv(file, parse_dates=['Date'])
    df.columns = ['Date', 'price']
    df.loc[:, 'price'] = pd.to_numeric(df['price'], errors='coerce')
    df.loc[:, 'Year'] = df['Date'].dt.year
    df.loc[:, 'name'] = 'GSE'
    return df


def get_all_data():
    stock_df = stock_price_data()
    gse_df = gse_index_data()
    final_df = pd.concat([stock_df, gse_df])
    return final_df


def company_description():
    ticker_file = os.path.join('data', 'ticker_descriptions.csv')
    description_df = pd.read_csv(ticker_file).fillna('Details Unavailable')

    def get_description(df, ticker):
        return df.loc[df.Ticker == ticker, 'Description'].iloc[0]

    tickers = set(description_df['Ticker'])
    description_dict = {ticker: get_description(
        description_df, ticker) for ticker in tickers}
    return description_dict


def share_code_func(df):
    codes = set(df['name'])
    codes.remove('GSE')
    return codes

# Import stock general information


def get_ticker_info(share_code):
    ticker_url = f'https://dev.kwayisi.org/apis/gse/equities/{share_code}'
    ticker_pull = requests.get(ticker_url)
    if ticker_pull.ok:
        return ticker_pull.json()
    else:
        raise ValueError


def modify_ticker_dict(ticker_dict):
    try:
        t_dict = ticker_dict.copy()
        t_dict['Name'] = t_dict['company']['name']
        t_dict['Sector'] = t_dict['company']['sector']
        del t_dict['company']
    except KeyError:
        return ticker_dict
    return t_dict


def share_charac_func(share_code):
    ticker_json = get_ticker_info(share_code)
    ticker_dict = modify_ticker_dict(ticker_json)
    return ticker_dict


def period_returns(ticker_, df):
    df_ = df.loc[(df['name'] == ticker_), ['Date', 'price']]
    df_['price'].fillna(method='ffill', inplace=True)
    df_.set_index('Date', inplace=True)
    return_dict = analib.calculate_periodic_returns(df_)
    return_name, return_list = zip(*return_dict.items())
    return return_name, return_list


# Create dictionary of industry dfs
def company_capital(stock_dict):
    df_stocks = pd.DataFrame.from_dict(stock_dict, orient='index')
    capital_df = df_stocks[['Name', 'Sector', 'capital']].copy()
    return capital_df.dropna()


def sector_capital(company_data):
    company_data.rename(columns={'capital': 'Capitalization'},
                        inplace=True)
    capital_industry = company_data.groupby(by='Sector', as_index=False).Capitalization.sum().sort_values(
        by='Capitalization')
    return capital_industry


def industry_share(company_data, ticker):
    sector = company_data.at[ticker, 'Sector']
    company_sector = company_data[company_data['Sector'] == sector]
    company_df = company_sector.reset_index()
    company_df.rename(columns={'index': 'Ticker'}, inplace=True)
    return company_df.rename(columns={'capital': 'Capitalization'})


# TODO: create function to calculate the number of shares for a 10,000 cedi investment at inception of stocks trading
def stock_share_func(df, ticker):
    stock_df = df.loc[df['name'] == ticker]
    stock_inception_date = stock_df['Date'].min()
    stock_inception_price = stock_df[[
        'price']][stock_df['Date'] == stock_inception_date].iat[0, 0]
    stock_inception_shares = 10000 / stock_inception_price
    return stock_inception_shares


def ticker_share(stock_price_df, share_code_list):
    ticker_share_dict = {share: stock_share_func(
        stock_price_df, share) for share in share_code_list}
    return ticker_share_dict


# TODO: Annual return function under development
# TODO: this should find its way to global analytics and possibly in to summary records
def annual_rate_func(df, stock):
    data = df.loc[df['name'] == stock].sort_values(by='Date')
    grouped = data.groupby(by='Year', as_index=False).last()
    filtered = grouped.loc[:, ['Year', 'price']].set_index('Year')
    ror = filtered.pct_change()
    ror.columns = ['Returns']
    return ror.reset_index().fillna(0)


def annual_return(stock_price_df, share_code_list):
    annual_return_df_dict = {share: annual_rate_func(
        stock_price_df, share) for share in share_code_list}
    return annual_return_df_dict


def get_input_params():
    print('Computing input parameters....')
    print('Getting data...')
    stock_price_df = get_all_data()
    print('Company descriptions...')
    company_profile = company_description()
    print('Share codelist....')
    share_code_list = share_code_func(stock_price_df)
    print('Stock character dict....')
    stock_charact_dict = {share: share_charac_func(
        share) for share in share_code_list}
    print("Capital per sector....")
    capital_per_sector = sector_capital(company_capital(stock_charact_dict))
    print('Ticker share....')
    tick_share = ticker_share(stock_price_df, share_code_list)
    print('Annual return...')
    all_codes = set(stock_price_df['name'])
    ann_return = annual_return(stock_price_df, all_codes)
    print('Done!')
    return (stock_price_df,
            company_profile,
            share_code_list,
            stock_charact_dict,
            capital_per_sector,
            tick_share,
            ann_return)


STOCK_PRICE_DF, COMPANY_PROFILE, SHARE_CODE_LIST, STOCK_CHARAC_DICT,\
    CAPITAL_PER_SECTOR, TICKER_SHARE, ANNUAL_RETURN = get_input_params()


def get_company_pie(ticker_name, ticker_company):
    industry_share_df = industry_share(
        company_capital(STOCK_CHARAC_DICT), ticker_name)
    company_share = industry_share_df['Capitalization'].loc[industry_share_df['Name'] == ticker_company].sum(
    )
    others_share = industry_share_df['Capitalization'].loc[industry_share_df['Name'] != ticker_company].sum(
    )
    share_cap_list = [company_share, others_share]
    #share_name_list = [ticker_company, 'Rest of Sector']
    pie = generic_pie(
        # labels=share_name_list,
        values=share_cap_list,
        #title='Market Share',
        pull=[0.2, 0]
    )
    pie.update_traces(marker=dict(
        colors=["rgb(0,38,100)", "rgb(220,220,220)"]))
    return pie


def get_company_line_graph(ticker_name):
    stock_df = STOCK_PRICE_DF.query('name == @ticker_name')
    stock_df.sort_values(by='Date', inplace=True)
    if ticker_name != 'GSE':
        stock_df.loc[:, 'Share Volume'] = TICKER_SHARE[ticker_name]
        stock_df.loc[:, 'Investment Value'] = stock_df['price'] * \
            stock_df['Share Volume']  # TODO: What is the assumption here?
        graph = generic_scatter(
            x=stock_df['Date'],
            y=stock_df['Investment Value']
        )
    else:
        graph = generic_scatter(
            x=stock_df['Date'],
            y=stock_df['price']
        )
    graph.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        height=200,
        plot_bgcolor="white"
    )
    graph.update_xaxes(showline=True, linecolor='black')
    graph.update_yaxes(showgrid=True, gridcolor="rgb(220,220,220)")
    graph.update_traces(marker_color="rgb(0,38,100)")
    return graph


def company_annual_return_bars(ticker_name):
    return_df = ANNUAL_RETURN[ticker_name]
    bar_fig = generic_bar(x=return_df['Year'], y=return_df['Returns']*100)
    bar_fig.update_layout(margin=dict(l=5, r=5, t=5, b=5),
                          height=200, plot_bgcolor="white")
    bar_fig.update_xaxes(showline=True, linecolor='black')
    bar_fig.update_yaxes(showgrid=True, gridcolor="rgb(220,220,220)")
    bar_fig.update_traces(marker_color="rgb(0,38,100)")
    return bar_fig


def company_compound_return_bars(ticker_name):
    compound_list = period_returns(ticker_name, STOCK_PRICE_DF)
    bar_comp_fig = generic_bar(x=compound_list[0], y=compound_list[1] * 100)
    bar_comp_fig.update_layout(margin=dict(l=5, r=5, t=5, b=5), height=200,
                               plot_bgcolor="white")
    bar_comp_fig.update_xaxes(showline=True, linecolor='black')
    bar_comp_fig.update_yaxes(showgrid=True, gridcolor="rgb(220,220,220)")
    bar_comp_fig.update_traces(marker_color="rgb(0,38,100)")
    return bar_comp_fig


def get_company_facts(ticker_json):
    company_df = pd.DataFrame(list(ticker_json['company'].items()), columns=[
                              'Attribute', 'Detail'])
    company_data = company_df.to_dict('records')
    company_col = [
        {'name': i, 'id': i} for i in ['Attribute', 'Detail']
    ]
    return company_data, company_col


def get_company_summary(ticker_name):
    stock_df = STOCK_PRICE_DF.query('name == @ticker_name').set_index('Date')
    stock_series = stock_df[['price']]
    summary = analib.series_summary(stock_series)
    return_df = ANNUAL_RETURN[ticker_name]
    summary['Number of Positive Years (Annual return)'] = sum(
        n > 0 for n in return_df['Returns'])
    summary['Number of Negative Years (Annual return)'] = sum(
        n < 0 for n in return_df['Returns'])
    summ_df = pd.DataFrame.from_dict(summary, orient='index').reset_index()
    summ_df.columns = ['Summary', '']
    data = summ_df.to_dict('records')
    cols = [
        {'name': i, 'id': i} for i in ['Summary', '']
    ]
    return data, cols


def individual_summary(ticker_name):
    stock_df = STOCK_PRICE_DF.query('name == @ticker_name').set_index('Date')
    stock_series = stock_df[['price']]
    ssummary = analib.series_current_summary(stock_series)
    return f"₵{ssummary[0]:.2f}|{ssummary[1]:.2%}"

# if __name__ =='__main__':
#     for t in SHARE_CODE_LIST:
#         summ = individual_summary(t)
#         print(f"{t}: {summ}")
