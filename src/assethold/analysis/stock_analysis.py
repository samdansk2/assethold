# Standard library imports
import os  # noqa

# Third party imports
import matplotlib.pyplot as plt  # noqa
import pandas as pd  # noqa
import pytz
from assetutilities.common.update_deep import update_deep_dictionary

# from assetutilities.common.visualization.visualization_common import VisualizationCommon

# visualization_common = VisualizationCommon()
# from stockhold.data.get_stock_data import GetStockData
# get_data = GetStockData()


class StockAnalysis():

    def __init__(self, cfg):
        self.cfg = cfg
        self.insider_analysis_by_relation_df = pd.DataFrame()
        self.insider_analysis_by_timeline_df = pd.DataFrame()
        self.call_effective_value_df = pd.DataFrame()
        self.call_effective_value_df_filtered = pd.DataFrame()
        self.insider_info = None
        self.insider_df_buy = pd.DataFrame()
        self.insider_df_sell = pd.DataFrame()
        self.status = {'insider': {}}

    def router(self, cfg,data):
        """
        Router function for StockAnalysis
        """
        analysis_output = {}
        status = {}
        analysis_status = {}
        analysis = {}
        if 'analysis' in cfg and cfg['analysis'].get('breakout', False):
            daily_data = data['daily']['data']
            daily_data['Date'] = pd.to_datetime(daily_data['Date'])
            start_date = '2018-09-01'
            end_date = '2024-09-30'
            daily_data = daily_data.loc[(daily_data['Date'] >= start_date) & (daily_data['Date'] <= end_date)]
            cfg, breakout_trend = self.breakout_trend_analysis(cfg, daily_data)

            analysis_output = {
                'breakout_trend': breakout_trend
            }

            analysis_status = {'breakout_trend': breakout_trend['status']}
            analysis = {'data': analysis_output, 'status': status}

        cfg_status_dict = {cfg['basename']: {'analysis': {'status': analysis_status}}}
        cfg = update_deep_dictionary(cfg, cfg_status_dict)

        return cfg, analysis

    def breakout_trend_analysis(self,cfg, daily_data):

        self.status.update({'breakout_trend': True})
        self.breakout_summary_array = []
        columns = ['Description', 'Value']
        breakout_df = pd.DataFrame(columns=columns)
        breakout_df.loc[len(breakout_df)] = self.check_if_price_above_150_and_200_moving(daily_data)
        breakout_df.loc[len(breakout_df)] = self.check_if_150_moving_above_200_moving(daily_data)
        breakout_df.loc[len(breakout_df)] = self.check_if_200_moving_up_for_1mo(daily_data)
        breakout_df.loc[len(breakout_df)] = self.check_if_50_day_above_150_and_200_moving(daily_data)
        breakout_df.loc[len(breakout_df)] = self.check_if_price_above_50_moving(daily_data)
        breakout_df.loc[len(breakout_df)] = self.check_if_price_above_1p3_52wk_low(daily_data)
        breakout_df.loc[len(breakout_df)] = self.check_if_price_near_52wk_high_range(daily_data)

        breakout_trend = {'data': breakout_df.to_dict(orient='records'), 'status': True} 
        
        self.save_plots(cfg,breakout_df,daily_data)
        #self.backtest(cfg, daily_data)
        
        return cfg, breakout_trend
    
    def save_plots(self,cfg,breakout_df,daily_data):
        
        self.plot_breakout_trend(cfg,breakout_df,daily_data)
        self.save_and_close_plots(cfg)

    def plot_breakout_trend(self, cfg, breakout_df, daily_data):

        # Standard library imports
        import re  # noqa

        # Third party imports
        import matplotlib.dates as mdates  # noqa

        daily_data['Date'] = pd.to_datetime(daily_data['Date'])

        def extract_analysis(value_str, description):
             
            if not isinstance(description, str):
                description = str(description)
    
            if isinstance(value_str, bool):
                return value_str, {}

            value_str = str(value_str)

            analysis = re.findall(r'\[.*?\]', value_str)
            value_cleaned = re.sub(r'\[.*?\]', '', value_str).strip()

            if value_cleaned in ['True', 'False']:
                value_cleaned = value_cleaned == 'True'

            description_cleaned = re.sub(r'\[.*?\]', '', description).strip()

            cleaned_analysis = {}
            if analysis:
                for part in analysis:
                    key = re.sub(r'.*\[(.*)\].*', r'\1', description) 
                    value = part.strip('[]').replace('mo.', '').replace('%', '').strip() 
                    if 'mo.' in key:
                        cleaned_analysis[key] = [f'{value}']
                    elif '%' in key:
                        cleaned_analysis[key] = [f'{value}']
                    else:
                        cleaned_analysis[key] = [value]

            return value_cleaned, cleaned_analysis if cleaned_analysis else {}

        breakout_analysis_df = pd.DataFrame(columns=['Description', 'Value', 'Analysis'])

        for index, row in breakout_df.iterrows():
            description = row['Description']
            value_str = row['Value']

            value_cleaned, analysis = extract_analysis(value_str, description)

            # Add to the cleaned DataFrame
            breakout_analysis_df.loc[index] = [
                re.sub(r'\[.*?\]', '', description).strip(), 
                value_cleaned,                                   
                analysis                                         
            ]

        print(breakout_analysis_df)

        breakout_daily_data_trend_df = pd.DataFrame(columns=[
        'Date', 'Close','Price Above 150 & 200 day avgs.', '150 day avg. above 200 day avg.',
        '200 day avg. uptrend for 1 mo [n mo.]', '50 day avg. Above 150 & 200 day avgs.',
        'Price Above 50 day avg. [x; y %]', 'Price 30% Above 52 wk low [% above]', 
        'Price within 25% of 52 wk high range [% value]', 'no_of_fails', 'plot_color'
            ])

        default_color = 'black'
        colors = []  # For plot color points 

        trend_data = []

        for index, row in daily_data.iterrows():

            if pd.isnull(row[['Close', '100_day_rolling', '50_day_rolling', '150_day_rolling', '200_day_rolling', '200_day_diff']]).all():
            # Assign default color if breakout data is missing
                colors.append(default_color)
                plot_color = default_color
                failed_conditions = 'Breakout data missing'
            else:
                failed_conditions = 0

                if not self.check_if_price_above_150_and_200_moving(daily_data)[1]:
                    failed_conditions += 1
                if not self.check_if_150_moving_above_200_moving(daily_data)[1]:
                    failed_conditions += 1
                if not self.check_if_200_moving_up_for_1mo(daily_data)[1]:
                    failed_conditions += 1
                if not self.check_if_50_day_above_150_and_200_moving(daily_data)[1]:
                    failed_conditions += 1
                if not self.check_if_price_above_50_moving(daily_data)[1]:
                    failed_conditions += 1
                if not self.check_if_price_above_1p3_52wk_low(daily_data)[1]:
                    failed_conditions += 1
                if not self.check_if_price_near_52wk_high_range(daily_data)[1]:
                    failed_conditions += 1
                
                plot_color = 'green' if failed_conditions == 0 else 'gold' if failed_conditions == 1 else 'red'
                colors.append(plot_color)


            trend_data.append({
            'Date': row['Date'],
            'Close': row['Close'],
            'Price Above 150 & 200 day avgs.': 'True' if self.check_if_price_above_150_and_200_moving(daily_data)[1] else 'False',
            '150 day avg. above 200 day avg.': 'True' if self.check_if_150_moving_above_200_moving(daily_data)[1] else 'False',
            '200 day avg. uptrend for 1 mo': 'True' if self.check_if_200_moving_up_for_1mo(daily_data)[1] else 'False',
            '50 day avg. Above 150 & 200 day avgs.': 'True' if self.check_if_50_day_above_150_and_200_moving(daily_data)[1] else 'False',
            'Price Above 50 day avg.': 'True' if self.check_if_price_above_50_moving(daily_data)[1] else 'False',
            'Price 30% Above 52 wk low': 'True' if self.check_if_price_above_1p3_52wk_low(daily_data)[1] else 'False',
            'Price within 25% of 52 wk high range': 'True' if self.check_if_price_near_52wk_high_range(daily_data)[1] else 'False',
            'no_of_fails': failed_conditions,
            'plot_color': plot_color
             })
                
            
        ticker = cfg['input']['ticker']
        breakout_daily_data_trend_df = pd.DataFrame(trend_data) 

        csv_file_path = f'src/assethold/tests/test_data/analysis/breakout_data_trend_{ticker}.csv'
        breakout_daily_data_trend_df.to_csv(csv_file_path, index=False)
           
              
        # Apply colors only when there's a change in plot color
        filtered_colors = [colors[0]]  # always include the first color
        filtered_dates = [daily_data['Date'].iloc[0]]  
        filtered_close = [daily_data['Close'].iloc[0]]  

        for i in range(1, len(colors)):
            if colors[i] != colors[i - 1]:  # apply color when there is change in plot color
                filtered_colors.append(colors[i])
                filtered_dates.append(daily_data['Date'].iloc[i])
                filtered_close.append(daily_data['Close'].iloc[i])
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(daily_data['Date'], daily_data['Close'], color='skyblue',label='Close Price')

        ax.scatter(filtered_dates, filtered_close, color= filtered_colors, s=70)

        ax.scatter([], [], color='green', label='breakout 0 fails')
        ax.scatter([], [], color='gold', label='breakout 1 fail')
        ax.scatter([], [], color='red', label='More than 1 fail')

        ax.set_title('Breakout Trend Analysis')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        ax.grid(True)

        #ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) # sets date in months 
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3)) # sets interval of 3 months

        plt.xticks(rotation=45) # rotates x-axis labels
        fig.autofmt_xdate() # auto formats x-axis date

        self.backtest(cfg, daily_data, breakout_daily_data_trend_df)

    def backtest(self,cfg, daily_data, breakout_daily_data_trend_df):
        
        portfolio = {
        'cash': 1000,           # Starting cash value (based on green condition)
        'stock_value': 0,       # Initial stock value
        'total_value': lambda: portfolio['cash'],   # Total portfolio value (initially cash only)
        'positions': 0          # No stock positions held initially
        }
        portfolio_history = []  # To store daily portfolio updates

        ticker = cfg['input']['ticker']

        for i, row in breakout_daily_data_trend_df.iterrows():
            breakout_color = row['plot_color'] 

            if breakout_color == 'green':
                stock_price = row['Close']
                cash_amount = 1000

                num_stocks = cash_amount // stock_price # Number of stocks you can buy with the cash amount

                cost = num_stocks * stock_price # Cost of buying the stocks

                portfolio['cash'] -= cost # cash balance after buying stocks

                portfolio['positions'] += num_stocks # number of stock positions held

            elif breakout_color == 'gold':

                self.sell_stock(portfolio, 200, row['Close'], limit_percent=50)

            elif breakout_color == 'red':

                self.sell_stock(portfolio, 500, row['Close'], limit_percent=20)

            # Update portfolio value based on current stock price
            self.update_portfolio_value(portfolio, row['Close'])

            self.log_portfolio(portfolio_history, portfolio, row['Date'])

        self.save_portfolio_history(portfolio_history, ticker)


    def sell_stock(self,portfolio, position_amount, stock_price, limit_percent):
        """
        Sell stock based on conditions in breakout_settings.
        """
        if portfolio['positions'] > 0:
            limit_positions = (limit_percent / 100) * portfolio['positions']
            if portfolio['positions'] > limit_positions:
                sell_amount = min(portfolio['positions'], position_amount)
                proceeds = sell_amount * stock_price 
                portfolio['positions'] -= sell_amount #number of stock positions held
                portfolio['cash'] += proceeds # cash balance after selling stocks


    def update_portfolio_value(self,portfolio, stock_price):
        """
        Update the portfolio value based on current stock price
        """
        portfolio['stock_value'] = portfolio['positions'] * stock_price # Value of stock holdings
        portfolio['total_value'] = portfolio['cash'] + portfolio['stock_value'] # Total portfolio value at the end of the day


    def log_portfolio(self,portfolio_history, portfolio, date):
        """
        Log the portfolio state.
        """
        portfolio_history.append({
            'Date': date,
            'Cash': portfolio['cash'],
            'Stock Value': portfolio['stock_value'],
            'Total Value': portfolio['total_value'],
            'Positions': portfolio['positions']
        })

    def save_portfolio_history(self,portfolio_history, ticker):

        log_df = pd.DataFrame(portfolio_history)
        csv_filename = f'src/assethold/tests/test_data/analysis/portfolio_report_{ticker}.csv'
        log_df.to_csv(csv_filename, index=False)
    

    def check_if_price_above_150_and_200_moving(self, breakout_df, close="Close"):

        description = 'Price Above 150 & 200 day avgs.'
        if breakout_df.iloc[-1][close] > breakout_df.iloc[-1]['150_day_rolling'] and breakout_df.iloc[-1][
                close] > breakout_df.iloc[-1]['200_day_rolling']:
            value = True
        else:
            value = False
        return [description, value]

    def check_if_150_moving_above_200_moving(self, breakout_df):

        description = '150 day avg. above 200 day avg.'
        if breakout_df.iloc[-1]['150_day_rolling'] > breakout_df.iloc[-1]['200_day_rolling']:
            value = True
        else:
            value = False
        return [description, value]

    def check_if_200_moving_up_for_1mo(self, breakout_df):

        description = '200 day avg. uptrend for 1 mo [n mo.]'
        no_of_months_trend_above = self.get_200_moving_up_for_n_mo(breakout_df)
        if no_of_months_trend_above >= 1:
            value = True
        else:
            value = False

        return [
            description,
            str(value) + " [{} mo.]".format(no_of_months_trend_above)
        ]

    def get_200_moving_up_for_n_mo(self, breakout_df):

        # Standard library imports
        import datetime
        breakout_df['200_day_diff'] = breakout_df['200_day_rolling'].diff(periods=1).values

        no_of_months_trend_above = 0
        half_months = 11
        for no_of_half_months in range(1, half_months):
            no_of_months_trend_above = 0.5 * (no_of_half_months - 1)
            days_period = 0.5 * no_of_half_months * 30
            start_time = breakout_df.Date.iloc[-1] + datetime.timedelta(
                days=-days_period)
            if start_time > breakout_df.Date.iloc[0]:
                breakout_df_temp = breakout_df[breakout_df.Date > start_time].copy()
                if breakout_df_temp['200_day_diff'].min() > 0:
                    no_of_months_trend_above = 0.5 * (no_of_half_months - 1)
                else:
                    break
            else:
                break

        return no_of_months_trend_above

    def check_if_50_day_above_150_and_200_moving(self, breakout_df):

        description = '50 day avg. Above 150 & 200 day avgs.'
        if breakout_df.iloc[-1]['50_day_rolling'] > breakout_df.iloc[-1][
                '150_day_rolling'] and breakout_df.iloc[-1]['50_day_rolling'] > breakout_df.iloc[
                    -1]['200_day_rolling']:
            value = True
        else:
            value = False
        return [description, value]

    def check_if_price_above_50_moving(self, breakout_df, close='Close'):

        description = 'Price Above 50 day avg. [x; y %]'
        price_above_50_moving = (breakout_df.iloc[-1][close] -
                                 breakout_df.iloc[-1]['50_day_rolling']).__round__(1)
        percent_price_above_50_moving = (
            (breakout_df.iloc[-1][close] - breakout_df.iloc[-1]['50_day_rolling']) /
            breakout_df.iloc[-1]['50_day_rolling'] * 100).__round__(0)
        if price_above_50_moving > 0:
            value = True
        else:
            value = False
        return [
            description,
            str(value) + " [{}; {}%]".format(price_above_50_moving,
                                             percent_price_above_50_moving)
        ]

    def check_if_price_above_1p3_52wk_low(self, breakout_df, close='Close'):

        # Standard library imports
        import datetime
        description = 'Price 30% Above 52 wk low [% above]'
        fiftyTwoWeekLow = breakout_df[breakout_df['Date'] > datetime.datetime.now(
            pytz.timezone('America/New_York')) +
                             datetime.timedelta(days=-365)].Close.min()
        percent_above_52wklow = ((breakout_df.iloc[-1][close] / fiftyTwoWeekLow - 1) *
                                 100).__round__(0)
        if percent_above_52wklow > 30:
            value = True
        else:
            value = False

        return [
            description,
            str(value) + " [{} %]".format(percent_above_52wklow)
        ]

    def check_if_price_near_52wk_high_range(self, breakout_df, close='Close'):
        
        # Standard library imports
        import datetime
        description = 'Price within 25% of 52 wk high range [% value]'
        fiftyTwoWeekHigh = breakout_df[breakout_df['Date'] > datetime.datetime.now(
            pytz.timezone('America/New_York')) +
                              datetime.timedelta(days=-365)].Close.max()
        percent_above_52wkhigh = ((breakout_df.iloc[-1][close] / fiftyTwoWeekHigh - 1) *
                                  100).__round__(0)
        if percent_above_52wkhigh > -25:
            value = True
        else:
            value = False

        return [
            description,
            str(value) + " [{} %]".format(percent_above_52wkhigh)
        ]
    

    def get_plot_name_path(self, cfg):
        
        file_name = cfg['Analysis']['file_name']
        plot_folder = os.path.join(cfg["Analysis"]["result_folder"], "Plot")

        plot_name_paths = [
            os.path.join(plot_folder, file_name)
        ]

        return plot_name_paths
    
    def save_and_close_plots(self, cfg):

        plot_name_paths = self.get_plot_name_path(cfg)
        # plt = plt_properties["plt"]
        for file_name in plot_name_paths:
            plt.savefig(file_name, dpi=800)

        plt.close()