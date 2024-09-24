# Standard library imports
import datetime
import json
import os
import logging 

# Third party imports
import pandas as pd
import yfinance as yf
from finvizfinance.quote import finvizfinance
from yahoo_fin.stock_info import tickers_dow, tickers_nasdaq, tickers_sp500
from assetutilities.common.update_deep import update_deep_dictionary
from assetutilities.common.visualization.visualization_templates import (
    VisualizationTemplates,
)
from assetutilities.engine import engine as aus_engine

viz_templates = VisualizationTemplates()


class GetStockData():

    def __init__(self, cfg):
        self.cfg = cfg
        self.status = {'insider': {}}
        self.days_rolling_array = [20, 100, 50, 150, 200]
        self.company_info = {'DataQuality': []}
        self.option_data = {}

        # self.sec_form = SECDataForm()
        # self.sec_form4 = pd.DataFrame()
        # self.sec_data_duration_years = 2

        self.inside_trader_df = pd.DataFrame()
        self.ratings_df = pd.DataFrame()
        self.option_data = {}

    def router(self, cfg):

        cfg, data = self.get_data(cfg)

        ticker = cfg['input']['ticker']
        daily_data = self.get_daily_data_by_ticker(cfg, ticker)
        daily_data_df = daily_data['data']
        daily_data_df['Date'] = pd.to_datetime(daily_data_df['Date']).dt.tz_localize(None)

        if "data" in cfg and cfg['data'].get('flag', False):
            """ 
            Condition check to overcome conflicts with analysis data
            """
            daily_data_df_copy = daily_data_df.tail(20).copy()
            self.save_results(cfg, daily_data_df_copy)

        return cfg,data

    def save_results(self, cfg, daily_data_df_copy):
        # file_name = cfg['input']['ticker'] + '_daily_data.csv'
        # file_name = os.path.join(cfg['Analysis']['result_folder'], file_name)
        file_name = cfg['input']['ticker'] + '_data_copy.csv'
        file_name = os.path.join(cfg['Analysis']['analysis_root_folder'], file_name)
        daily_data_df_copy.to_csv(file_name, index=False)
        
        csv_groups = [{'file_name': file_name, 'label': ''}]
        self.save_plots(cfg, csv_groups)

    def save_plots(self, cfg, csv_groups):
        
        self.save_daily_data_plot(cfg, csv_groups.copy())

    def valid_ticker(self, ticker=None):
        return True

    def get_data(self, cfg=None):
        ticker = cfg['input']['ticker']

        daily = self.get_daily_data_by_ticker(cfg, ticker)
        daily = self.add_rolling_averages(daily)

        info = self.get_company_data_by_ticker(ticker)
        info = self.add_stats_to_info(daily, info)

        insider = self.get_insider_information(cfg, ticker)

        ratings = self.get_ratings()
        options = self.get_options_data()
        institutions = self.get_yf_institutions(ticker=ticker)

        data = {'daily': daily, 'info': info, 'insider': insider, 'ratings': ratings, 'options': options, 'institutions': institutions}

        data_status = {'daily': daily['status'], 'info': info['status'], 'insider': insider['status']}
        cfg_status_dict = {cfg['basename']: {'data': {'status': data_status}}}
        cfg = update_deep_dictionary(cfg, cfg_status_dict)
        
        return cfg, data

    def get_EOD_data_from_yfinance(self, cfg, ticker):
        period = cfg['input']['data_settings']['eod']['period']
        yf_ticker = yf.Ticker(str(ticker))
        company_info = yf_ticker.info
        df = yf_ticker.history(period=period)

        return df

    def add_rolling_averages(self, daily):
        df = daily['data']
        for days_rolling in self.days_rolling_array:
            df[str(days_rolling) +
               '_day_rolling'] = df.Close.rolling(window=days_rolling).mean()

        daily['data'] = df

        return daily

    def get_company_data_by_ticker(self, ticker):
        yf_ticker = yf.Ticker(str(ticker))
        info_data = yf_ticker.info

        info = {'data': info_data, 'status': True}

        return info

    def add_stats_to_info(self, daily, info_data):
        daily_df = daily['data']
        num_years = ((daily_df.Date.max() - daily_df.Date.min()).days /
                        365.25).__round__(1)
        
        info_data = info_data['data']
        fiftyTwoWeekLow = info_data['fiftyTwoWeekLow']
        fiftyTwoWeekHigh = info_data['fiftyTwoWeekHigh']
        info_data['DataDuration'] =  num_years
        info_data.update({'fiftyTwoWeekLow': fiftyTwoWeekLow})
        info_data.update({'fiftyTwoWeekHigh': fiftyTwoWeekHigh})

        info = {'data': info_data.copy(), 'status': True}
        
        return info

    def get_insider_information(self, cfg, ticker):
        status = False
        insider_info_finviz = self.get_insider_information_from_finviz(cfg,ticker)
        sec_data = self.get_sec_data(ticker)
        sec_form4 = sec_data.get('sec_form4')
        if len(sec_form4) > 0:
            insider_df = sec_form4
            insider_df = self.insider_data_clean_and_add_share_ratio(insider_df)
            status = True
        elif len(insider_info_finviz) > 0:
            insider_df = insider_info_finviz
            insider_df = self.insider_data_clean_and_add_share_ratio(insider_df)
            status = True
        else:
            self.status.update({'insider_info': False})
            insider_df = pd.DataFrame()

        insider = {'data': insider_df, 'status': status}

        return insider



    def get_stock_price_data(self, cfg):
        try:
            self.status.update({'price': True})
            ticker = cfg['stocks'][0]['ticker']
            self.get_data_from_yfinance(ticker)
        except:
            self.status.update({'price': False})
            raise ("No valid data source found")

    def get_insider_information_from_finviz(self, cfg, stock_ticker):
        self.status['insider']['finviz'] = {}
        try:
            fv_ticker = finvizfinance(stock_ticker)
            insider_info_finviz = fv_ticker.ticker_inside_trader()
            current_year = datetime.datetime.now().year
            insider_info_finviz['SEC Form 4'] = insider_info_finviz[
                'SEC Form 4'].apply(lambda x: str(current_year) + ' ' + x)
            insider_info_finviz['SEC Form 4'] = pd.to_datetime(
                insider_info_finviz['SEC Form 4'], infer_datetime_format=True)
            insider_info_finviz['SEC Form 4'] = insider_info_finviz[
                'SEC Form 4'].apply(lambda x: x if x < datetime.datetime.now()
                                    else x + datetime.timedelta(days=-365))
            insider_info_finviz['Date'] = insider_info_finviz['SEC Form 4']
            start_date = insider_info_finviz['Date'].min().strftime("%m-%d-%Y")
            end_date = insider_info_finviz['Date'].max().strftime("%m-%d-%Y")
            updated_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            self.status['insider']['finviz'].update({
                'status': True,
                'start': start_date,
                'end': end_date,
                'updated_time': updated_time
            })
            insider_info_finviz.drop(['SEC Form 4'],
                                     axis=1,
                                     errors='ignore',
                                     inplace=True)
        except:
            insider_info_finviz = pd.DataFrame()
            self.status['insider']['finviz'].update({'status': False})

        return insider_info_finviz

    def get_ratings(self):
        self.status.update({'ratings': True})
        try:
            self.ratings_df = self.fv_ticker.TickerOuterRatings()
        except:
            self.status.update({'ratings': False})
            self.ratings_df = pd.DataFrame()

    def get_options_data(self):
        self.status.update({'options': True})
        try:
            option_dates = list(self.yf_ticker.options)
            for date in option_dates:
                option_chain = self.get_option_data_by_date(date)
                self.option_data.update({date: option_chain})
        except Exception:
            self.status.update({'options': False})
            self.option_data = {}

    def get_option_data_by_date(self, date):
        option_chain = self.yf_ticker.option_chain(date)
        option_chain_dict = {
            'calls': option_chain.calls,
            'puts': option_chain.puts
        }
        return option_chain_dict

    def get_data_from_tiingo(self):
        # Third party imports
        import pandas_datareader as pdr
        api_key = '512e3063ad18b5116a83cf7ce7d852af4181917c'
        self.stock_data_array = []
        for stock_info in self.cfg.stocks:
            stock_ticker = stock_info['ticker']
            self.company_info['stock_ticker'] = stock_ticker
            df = pdr.get_data_tiingo(stock_ticker, api_key=api_key)
            df['date'] = [index_value[1] for index_value in df.index]
            for days_rolling in self.days_rolling_array:
                df[str(days_rolling) + '_day_rolling'] = df.close.rolling(
                    window=days_rolling).mean()
            self.stock_data_array.append(df)

    def get_screened_stocks(self):
        # Third party imports
        from finvizfinance.screener.overview import Overview
        finviz_overview = Overview()
        filters_dict = {'Exchange': 'AMEX', 'Sector': 'Basic Materials'}
        finviz_overview.set_filter(filters_dict=filters_dict)
        df = finviz_overview.ScreenerView()
        df.head()

    def get_daily_data_by_ticker(self, cfg, ticker):
        period = cfg.get('period', '5y')
        if ticker is not None:
            yf_ticker = yf.Ticker(str(ticker))
            df = yf_ticker.history(period=period)
            df.reset_index(inplace=True)

        daily = {'data': df, 'status': True}
        return daily

    def add_rolling_averages_to_df(self, df):
        days_rolling_array = self.days_rolling_array
        for days_rolling in days_rolling_array:
            df[str(days_rolling) + '_day_rolling'] = df.Close.rolling(
                window=days_rolling).mean()

        return df

    def get_data_from_yfinance(self, ticker=None):
        period = self.cfg.get('period', '5y')
        self.stock_data_array = []
        period = self.cfg.get('period', '5y')
        for stock_info in self.cfg['input']['data']['eod']['stocks']:
            stock_ticker = stock_info['ticker']
            self.yf_ticker = yf.Ticker(str(stock_ticker))
            self.company_info['stock_ticker'] = stock_ticker
            self.company_info['info'] = self.yf_ticker.info
            df = self.yf_ticker.history(period=period)
            df.reset_index(inplace=True)
            for days_rolling in self.days_rolling_array:
                df[str(days_rolling) + '_day_rolling'] = df.Close.rolling(
                    window=days_rolling).mean()
            self.stock_data_array.append(df)

    def get_data_from_morningstar(self):
        data_source = 'morningstar'

        # Standard library imports
        import datetime

        # Third party imports
        import pandas_datareader.data as web

        start = datetime.datetime(2010, 1, 1)
        end = datetime.datetime(2013, 1, 27)
        f = web.DataReader('OXY', data_source, start, end)

        print(web.DataReader('OXY', data_source, start, end))

    def get_data_from_iex(self):
        days_rolling_array = self.days_rolling_array
        # Standard library imports
        import os
        os.environ["IEX_API_KEY"] = self.cfg.default['data_sources']['iex'][
            'api_key']
        # {'tiingo': {'flag': None}}
        # Standard library imports
        from datetime import datetime, timedelta

        # Third party imports
        import pandas_datareader.data as web
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5479)

        self.stock_data_array = []
        for stock_info in self.cfg.stocks:
            stock_ticker = stock_info['ticker']
            df = web.DataReader(stock_ticker, 'iex', start_date, end_date)
            df['date'] = [index_value for index_value in df.index]
            for days_rolling in days_rolling_array:
                df[str(days_rolling) + '_day_rolling'] = df.close.rolling(
                    window=days_rolling).mean()
            self.stock_data_array.append(df)

    def get_sec_data(self, ticker):
        try:
            sec_form4 = self.sec_form.get_sec_form_data(
                ticker, cfg_sec=self.cfg["cfg_sec"])
            sec_data = {'sec_form4': sec_form4}
        except:
            sec_data = {'sec_form4': []}
        return sec_data

    def get_tickers_dow(self):
        tickers = tickers_dow()
        return tickers

    def get_tickers_nasdaq(self):
        tickers = tickers_nasdaq()
        return tickers

    def get_tickers_sp500(self):
        tickers = tickers_sp500()
        return tickers

    def insider_data_clean_and_add_share_ratio(self, insider_df):
        insider_df.drop(['SEC Form 4', 'Insider_id'],
                        axis=1,
                        inplace=True,
                        errors='ignore')
        insider_df['start_shares'] = 0
        insider_df['share_holding_ratio'] = 0
        insider_df['average_cost'] = 0

        for row_index in range(0, len(insider_df)):
            df_temp = insider_df.iloc[[row_index]]
            start_shares, share_holding_ratio, average_cost = self.sec_data_get_economic_analysis_for_subset_df(
                df_temp)
            insider_df['start_shares'].iloc[row_index] = start_shares
            insider_df['share_holding_ratio'].iloc[
                row_index] = share_holding_ratio
            insider_df['average_cost'].iloc[row_index] = average_cost

        return insider_df

    def sec_data_get_economic_analysis_for_subset_df(self, df):
        end_shares = df['#Shares Total'].iloc[0]
        noShares = df['#Shares'].sum()
        if df['Transaction'].iloc[-1] in ['Sell', 'Sale']:
            start_shares = df['#Shares Total'].iloc[-1] + noShares
        else:
            start_shares = df['#Shares Total'].iloc[-1] - noShares

        if start_shares > 0:
            share_holding_ratio = (end_shares / start_shares).__round__(2)
        else:
            share_holding_ratio = 1.01

        try:
            average_cost = (df['#Shares'] *
                            df['Cost']).sum() / df['#Shares'].sum()
            average_cost = round(average_cost, 3)
        except:
            average_cost = None

        return start_shares, share_holding_ratio, average_cost

    def get_sec_ticker_data(self):

        # Reader imports
        from assethold.finance_components_get_SEC_data import SECDataTicker

        sec_ticker = SECDataTicker()

        company_tickers_json = sec_ticker.get_company_tickers()
        company_tickers = json.loads(company_tickers_json)

        company_tickers_exchange_json = sec_ticker.get_company_tickers_exchange(
        )
        company_tickers_exchange = json.loads(company_tickers_exchange_json)

        company_tickers_mf_json = sec_ticker.get_company_tickers_mf()
        company_tickers_mf = json.loads(company_tickers_mf_json)

        sec_ticker_data = {
            'company_tickers': company_tickers,
            'company_tickers_exchange': company_tickers_exchange,
            'company_tickers_mf': company_tickers_mf
        }

        return sec_ticker_data
    

    def get_yf_institutions(self, ticker):
        
        self.yf_ticker = yf.Ticker(str(ticker))
        self.institutional_holders = self.yf_ticker.get_institutional_holders(proxy=None, as_dict=False)
        self.major_holders = self.yf_ticker.get_major_holders(proxy=None, as_dict=False)

    def get_institutional_holders(self, proxy=None, as_dict=False):
        self._holders.proxy = proxy or self.proxy
        data = self._holders.institutional
        if data is not None:
            if as_dict:
                return data.to_dict()
            return data
        
    def get_major_holders(self, proxy=None, as_dict=False):
        self._holders.proxy = proxy or self.proxy
        data = self._holders.major
        if as_dict:
            return data.to_dict()
        return data
    
    def save_daily_data_plot(self, cfg, csv_groups):

        import matplotlib.pyplot as plt
        plot_yml = viz_templates.get_xy_line_csv(cfg['Analysis'].copy())

        plot_yml['data']['groups'] = csv_groups
        columns= { 'x': ['Date'], 'y': ['Volume'] }
        plot_yml['master_settings']['groups']['columns'] = columns

        # dnow = datetime.datetime.now()
        # dstart = datetime.datetime(2024, 7, 1)
        # x_limits = [dstart, dnow]

        #transform = [{ 'column': 'length', 'scale': 0.0254, 'shift': 0 }]


        #plot_yml['master_settings']['groups']['transform'] = transform

        settings = {'file_name': cfg['input']['ticker'] + '_daily_data', 
                    'title': 'Daily data by ticker',
                    'xlabel': 'date',
                    'ylabel': 'Volume',
                    }
        plot_yml['settings'].update(settings)
        aus_engine(inputfile=None, cfg=plot_yml, config_flag=False)

    
