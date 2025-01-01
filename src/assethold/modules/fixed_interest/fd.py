
#TODO - implement the FixedDeposit class

def calculate_interest(self, cfg, prices_data, total_investment):
        """
        Simple and compound interest based on cumulative investment.
        """
        annual_rate =  0.05 # sample interest rate of 5%
        principal = total_investment
        start_date = prices_data['Date'].iloc[0]
        end_date = prices_data['Date'].iloc[-1]
        time_in_years = (end_date - start_date).days / 365

        # SI 
        simple_interest = principal * annual_rate * time_in_years

        # CI
        compound_interest = principal * ((1 + annual_rate) ** time_in_years - 1)

        return simple_interest, compound_interest