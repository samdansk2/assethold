# Standard library imports
import pandas as pd #noqa
import matplotlib.pyplot as plt #noqa

import os #noqa

# Third party imports
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
        if 'analysis' in cfg and cfg['analysis'].get('flag', False):
            daily_data = data['daily']['data']
            daily_data = daily_data.tail(20)
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
        df = pd.DataFrame(columns=columns)
        df.loc[len(df)] = self.check_if_price_above_150_and_200_moving(daily_data)
        df.loc[len(df)] = self.check_if_150_moving_above_200_moving(daily_data)
        df.loc[len(df)] = self.check_if_200_moving_up_for_1mo(daily_data)
        df.loc[len(df)] = self.check_if_50_day_above_150_and_200_moving(daily_data)
        df.loc[len(df)] = self.check_if_price_above_50_moving(daily_data)
        df.loc[len(df)] = self.check_if_price_above_1p3_52wk_low(daily_data)
        df.loc[len(df)] = self.check_if_price_near_52wk_high_range(daily_data)

        breakout_trend = {'data': df.to_dict(orient='records'), 'status': True} 
        
        self.save_plots(cfg,df,daily_data)
        
        return cfg, breakout_trend
    
    def save_plots(self,cfg,df,daily_data):
        
        self.plot_breakout_trend(cfg,df,daily_data)
        self.save_and_close_plots(cfg)

    def plot_breakout_trend(self, cfg, df, daily_data):
        """
        breakout trend with colored dots based on breakout criteria.
        """
        import matplotlib.dates as mdates # noqa
        import re # noqa

        daily_data['Date'] = pd.to_datetime(daily_data['Date'])

        default_color = 'black'
        colors = []  

        for index, row in daily_data.iterrows():

            # Check if all the key columns contains NaN ( breakout data missing for that day )
            if pd.isnull(row[['Close', '100_day_rolling', '50_day_rolling', '150_day_rolling', '200_day_rolling', '200_day_diff']]).all():
                # Missing data, assign gray color
                colors.append(default_color)
            else:
                failed_conditions = 0
                
            # check for breakout conditions ( boolean )
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

                if failed_conditions == 0:
                    colors.append('green')  
                elif failed_conditions == 1:
                    colors.append('gold')
                else:
                    colors.append('red')

        def extract_analysis(value_str, description):
             
            if not isinstance(description, str):
                description = str(description)
    
            if isinstance(value_str, bool):
                # If the value is already a boolean, just return it and an empty dictionary
                return value_str, {}

            value_str = str(value_str)

            # Extract analysis from Value using regex
            analysis = re.findall(r'\[.*?\]', value_str)
            value_cleaned = re.sub(r'\[.*?\]', '', value_str).strip()

            if value_cleaned in ['True', 'False']:
                value_cleaned = value_cleaned == 'True'

            description_cleaned = re.sub(r'\[.*?\]', '', description).strip()

            cleaned_analysis = {}
            if analysis:
                for part in analysis:
                    key = re.sub(r'.*\[(.*)\].*', r'\1', description)  # Extract key
                    value = part.strip('[]').replace('mo.', '').replace('%', '').strip()  # Clean the value
                    if 'mo.' in key:
                        cleaned_analysis[key] = [f'{value}']
                    elif '%' in key:
                        cleaned_analysis[key] = [f'{value}']
                    else:
                        cleaned_analysis[key] = [value]

            return value_cleaned, cleaned_analysis if cleaned_analysis else {}

        # New DataFrame with desired columns
        breakout_analysis_trend_df = pd.DataFrame(columns=['Description', 'Value', 'Analysis'])

        for index, row in df.iterrows():
            description = row['Description']
            value_str = row['Value']

            # Extract the boolean value and analysis details
            value_cleaned, analysis = extract_analysis(value_str, description)

            # Add to the cleaned DataFrame
            breakout_analysis_trend_df.loc[index] = [
                re.sub(r'\[.*?\]', '', description).strip(),     # Keep the same description
                value_cleaned,                                   # Cleaned Value (True/False)
                analysis                                         # Extracted Analysis details as a dictionary
            ]

        print(breakout_analysis_trend_df)    

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(daily_data['Date'], daily_data['Close'], color='skyblue',label='Close Price')

        ax.scatter(daily_data['Date'], daily_data['Close'], color=colors, s=70,label='Breakout Trend')

        ax.set_title('Breakout Trend Analysis')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        ax.grid(True)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%d')) # sets date in month name and day
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2)) # sets interval of 2 days

        plt.xticks(rotation=45) # rotates x-axis labels
        fig.autofmt_xdate() # auto formats x-axis date
    

    def check_if_price_above_150_and_200_moving(self, df, close="Close"):

        description = 'Price Above 150 & 200 day avgs.'
        if df.iloc[-1][close] > df.iloc[-1]['150_day_rolling'] and df.iloc[-1][
                close] > df.iloc[-1]['200_day_rolling']:
            value = True
        else:
            value = False
        return [description, value]

    def check_if_150_moving_above_200_moving(self, df):

        description = '150 day avg. above 200 day avg.'
        if df.iloc[-1]['150_day_rolling'] > df.iloc[-1]['200_day_rolling']:
            value = True
        else:
            value = False
        return [description, value]

    def check_if_200_moving_up_for_1mo(self, df):

        description = '200 day avg. uptrend for 1 mo [n mo.]'
        no_of_months_trend_above = self.get_200_moving_up_for_n_mo(df)
        if no_of_months_trend_above >= 1:
            value = True
        else:
            value = False

        return [
            description,
            str(value) + " [{} mo.]".format(no_of_months_trend_above)
        ]

    def get_200_moving_up_for_n_mo(self, df):

        # Standard library imports
        import datetime
        df['200_day_diff'] = df['200_day_rolling'].diff(periods=1).values

        no_of_months_trend_above = 0
        half_months = 11
        for no_of_half_months in range(1, half_months):
            no_of_months_trend_above = 0.5 * (no_of_half_months - 1)
            days_period = 0.5 * no_of_half_months * 30
            start_time = df.Date.iloc[-1] + datetime.timedelta(
                days=-days_period)
            if start_time > df.Date.iloc[0]:
                df_temp = df[df.Date > start_time].copy()
                if df_temp['200_day_diff'].min() > 0:
                    no_of_months_trend_above = 0.5 * (no_of_half_months - 1)
                else:
                    break
            else:
                break

        return no_of_months_trend_above

    def check_if_50_day_above_150_and_200_moving(self, df):

        description = '50 day avg. Above 150 & 200 day avgs.'
        if df.iloc[-1]['50_day_rolling'] > df.iloc[-1][
                '150_day_rolling'] and df.iloc[-1]['50_day_rolling'] > df.iloc[
                    -1]['200_day_rolling']:
            value = True
        else:
            value = False
        return [description, value]

    def check_if_price_above_50_moving(self, df, close='Close'):

        description = 'Price Above 50 day avg. [x; y %]'
        price_above_50_moving = (df.iloc[-1][close] -
                                 df.iloc[-1]['50_day_rolling']).__round__(1)
        percent_price_above_50_moving = (
            (df.iloc[-1][close] - df.iloc[-1]['50_day_rolling']) /
            df.iloc[-1]['50_day_rolling'] * 100).__round__(0)
        if price_above_50_moving > 0:
            value = True
        else:
            value = False
        return [
            description,
            str(value) + " [{}; {}%]".format(price_above_50_moving,
                                             percent_price_above_50_moving)
        ]

    def check_if_price_above_1p3_52wk_low(self, df, close='Close'):

        # Standard library imports
        import datetime
        description = 'Price 30% Above 52 wk low [% above]'
        fiftyTwoWeekLow = df[df['Date'] > datetime.datetime.now(
            pytz.timezone('America/New_York')) +
                             datetime.timedelta(days=-365)].Close.min()
        percent_above_52wklow = ((df.iloc[-1][close] / fiftyTwoWeekLow - 1) *
                                 100).__round__(0)
        if percent_above_52wklow > 30:
            value = True
        else:
            value = False

        return [
            description,
            str(value) + " [{} %]".format(percent_above_52wklow)
        ]

    def check_if_price_near_52wk_high_range(self, df, close='Close'):
        
        # Standard library imports
        import datetime
        description = 'Price within 25% of 52 wk high range [% value]'
        fiftyTwoWeekHigh = df[df['Date'] > datetime.datetime.now(
            pytz.timezone('America/New_York')) +
                              datetime.timedelta(days=-365)].Close.max()
        percent_above_52wkhigh = ((df.iloc[-1][close] / fiftyTwoWeekHigh - 1) *
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