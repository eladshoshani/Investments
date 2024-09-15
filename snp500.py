from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

# Assuming monthly_closing_prices is available (this is the monthly price data)
INITIAL_CAPITAL = 1_000_000

# Parameters
INVESTMENT_PERIODS = [1, 5, 10, 25]  # Years

def get_monthly_closing_prices() -> list[float]:
    snp500_prices = pd.read_csv('SPX.csv')

    # Convert the 'Date' column to datetime
    snp500_prices['Date'] = pd.to_datetime(snp500_prices['Date'])

    # Set the 'Date' column as index (optional, but useful for grouping)
    snp500_prices.set_index('Date', inplace=True)

    # Group by year and month, and take the last closing price of each month
    monthly_closing_prices = snp500_prices['Close'].resample('M').last()

    # Return the list of monthly closing prices
    return monthly_closing_prices.tolist()
def lump_sum_return(prices, start_idx: int, investment_period: int):
    start_price = prices[start_idx]
    end_price = prices[start_idx + investment_period - 1]
    return (end_price - start_price) / start_price


def get_dca_return_calculator(buying_period: Optional[int] = None, money_market_fund_annual_interest: float = 0.03):
    def calculator(prices: list[float], start_idx: int, investment_period: int):
        local_buying_period = buying_period if buying_period is not None else investment_period
        num_shares = 0
        money_market_fund_balance = INITIAL_CAPITAL
        monthly_fund_interest_rate = (1 + money_market_fund_annual_interest) ** (1 / 12) - 1
        # Buy stocks each month in the buying period:
        for i in range(local_buying_period):
            money_market_fund_balance *= 1 + monthly_fund_interest_rate
            invest_this_month = money_market_fund_balance / (local_buying_period - i)
            # Withdraw from the fund and invest in the stock
            money_market_fund_balance -= invest_this_month
            num_shares += invest_this_month / prices[start_idx + i]
        money_at_the_end = num_shares * prices[start_idx + investment_period - 1]
        return (money_at_the_end - INITIAL_CAPITAL) / INITIAL_CAPITAL
    return calculator


def get_y_axis(calc_func, prices, investment_period):
    return [calc_func(prices, i, investment_period) for i in range(len(prices) - investment_period)]

def main():
    prices = get_monthly_closing_prices()
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.ravel()  # Flatten the 2D array of axes


    dca_return = get_dca_return_calculator(money_market_fund_annual_interest=0.03)   # in the future test also shorter buying periods
    for idx, years in enumerate(INVESTMENT_PERIODS):
        returns_lump_sum = get_y_axis(lump_sum_return, prices, investment_period=years * 12)
        returns_dca = get_y_axis(dca_return, prices, investment_period=years * 12)

        # Plot the returns
        axes[idx].plot(returns_lump_sum, "o-", color="orange", markersize=3, label="Lump-Sum")
        axes[idx].plot(returns_dca, "o-", color="blue", markersize=3, label="DCA")
        axes[idx].set_title(f"{years} Year Investment Period", fontsize=14)
        axes[idx].set_xlabel("Time (months)", fontsize=12)
        axes[idx].set_ylabel("Annual Return", fontsize=12)
        axes[idx].grid(True, linestyle='--', alpha=0.7)
        axes[idx].legend()

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
