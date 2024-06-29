"""
This module is used to estimate the return on investment when buying an apartment, renting it,
and selling it after a few years.

The calculation steps (in high level) are:
1. Calculate the monthly cashflows from the apartment (rent - mortgage payment).
2. Calculate the missed gains from the negative cashflows that could have been invested in the market.
3. Calculate left cash when selling the apartment (sell price - mortgage balance - sell expenses - missed market gains).
4. Calculate the average annual return on the investment.

Notes and assumptions:
    - The calculation does not take into account the tax implications of the investment, and inflation.
        * Most real-estate investments are tax-free in Israel (for a single apartment).
        * When providing the annual market return in the assumptions, it should be after accounting for tax.
            For example, if the market return is 10% and the tax is 25%, then you should provide 7.5%.
        * Not accounting for inflation is a simplification - every investment is affected by inflation...
    - The calculation assumes that the apartment is rented for the entire investment term.
    - The calculation assumes that the apartment is sold at the end of the investment term.
    - The calculation assumes that the rent increases every few years.
    - The calculation assumes that the mortgage is paid in equal monthly payments.
    - The calculation assumes that the mortgage interest is constant throughout the investment term.
        * In reality, the interest rate might change, and the mortgage might be refinanced.
        * As we don't have a crystal ball, we can't predict the future interest rates.
"""

from dataclasses import dataclass
from typing import Optional

from mortgage import Loan

SELL_EXPENSES_PERCENTAGE = 0.025 * 1.18  # 2.5% of the sell price (+VAT)


@dataclass
class Assumptions:
    investment_term: int
    annual_apartment_price_growth: float
    annual_rent_percentage: float
    rent_increase_delta: int  # Number of years between rent increases
    annual_market_return: float
    buy_expenses: float  # Expenses when buying the apartment (for example for a lawyer, etc.)
    new_apartment_current_value: Optional[float] = None  # Relevant for Pinuy-Binuy investments

    @staticmethod
    def calc_sell_expenses(sell_price: float) -> float:
        return sell_price * SELL_EXPENSES_PERCENTAGE


@dataclass
class Mortgage:
    apartment_buy_price: float
    apartment_assessor_price_evaluation: float
    financing_percentage: float  # for example, 0.75 for 75%
    interest_rate: float  # annual interest rate (for example, 0.03 for 3%)
    loan_term: int  # number of years

    def __post_init__(self):
        self.loan = Loan(
            principal=self.loan_amount,
            interest=self.interest_rate,
            term=self.loan_term,
            currency="₪",
        )

    @property
    def loan_amount(self) -> float:
        return min(self.apartment_buy_price, self.apartment_assessor_price_evaluation) * self.financing_percentage

    @property
    def monthly_payment(self) -> float:
        return float(self.loan.monthly_payment)


@dataclass
class ApartmentInvestmentSummary:
    initial_capital: float
    final_capital: float
    investment_term: int
    buy_price: float
    sell_price: float
    interest_paid_on_mortgage: float
    monthly_distinct_cashflows: list[float]
    # Also take into account missed gains from negative cashflows that could have been invested in the market:
    total_loss_from_cashflows: float

    @property
    def avg_annual_return(self) -> float:
        return (self.final_capital / self.initial_capital) ** (1 / self.investment_term) - 1

    def __str__(self):
        return (
            f"Average annual return: {self.avg_annual_return:.2%}\n"
            f"Initial capital: {self.initial_capital}\n"
            f"Final capital: {self.final_capital}\n"
            f"Buy price: {self.buy_price}\n"
            f"Sell price: {self.sell_price}\n"
            f"Investment term: {self.investment_term} years\n"
            f"Interest paid on mortgage: {self.interest_paid_on_mortgage}\n"
            f"Monthly (distinct) cashflows:\n{self.monthly_distinct_cashflows}\n"
            f"Total loss from cashflows: {self.total_loss_from_cashflows}\n"
        )


def monthly_cashflows(investment_term: int, mortgage: Mortgage, assumptions: Assumptions) -> list[float]:
    cashflows = []
    rent_per_month = (mortgage.apartment_assessor_price_evaluation * assumptions.annual_rent_percentage) / 12
    for year in range(1, investment_term + 1):
        cashflows += [rent_per_month - mortgage.monthly_payment] * 12
        if year % assumptions.rent_increase_delta == 0:
            rent_per_month *= (1 + assumptions.annual_apartment_price_growth) ** assumptions.rent_increase_delta

    return cashflows


def investment_estimation(
    mortgage: Mortgage,
    assumptions: Assumptions,
) -> ApartmentInvestmentSummary:
    apartment_sell_price = (assumptions.new_apartment_current_value or mortgage.apartment_buy_price) * (
        (1 + assumptions.annual_apartment_price_growth) ** assumptions.investment_term
    )

    # Calculate the loss (or gain) from not investing the (probably negative) cashflows in the market each month
    cashflows = monthly_cashflows(assumptions.investment_term, mortgage, assumptions)
    market_monthly_return = (1 + assumptions.annual_market_return) ** (1 / 12) - 1
    market_capital_missed_gains = 0
    market_capital_gains = 0
    for cashflow in cashflows:
        if cashflow < 0:
            market_capital_missed_gains -= cashflow
        else:
            market_capital_gains += cashflow
        market_capital_gains *= 1 + market_monthly_return
        market_capital_missed_gains *= 1 + market_monthly_return
    total_loss_from_cashflows = market_capital_missed_gains - market_capital_gains

    # Calculate the profit from the apartment investment
    initial_invested_capital = assumptions.buy_expenses + (mortgage.apartment_buy_price - mortgage.loan_amount)
    mortgage_end_state = mortgage.loan.schedule(assumptions.investment_term * 12)
    final_capital = (
        apartment_sell_price
        - assumptions.calc_sell_expenses(apartment_sell_price)
        - float(mortgage_end_state.balance)
        - total_loss_from_cashflows
    )
    ret = ApartmentInvestmentSummary(
        initial_capital=initial_invested_capital,
        final_capital=final_capital,
        investment_term=assumptions.investment_term,
        buy_price=mortgage.apartment_buy_price,
        sell_price=apartment_sell_price,
        interest_paid_on_mortgage=float(mortgage_end_state.total_interest),
        monthly_distinct_cashflows=sorted(set(cashflows)),
        total_loss_from_cashflows=total_loss_from_cashflows,
    )
    return ret


def main():
    estimation = investment_estimation(
        mortgage=Mortgage(
            apartment_buy_price=1_930_000,
            apartment_assessor_price_evaluation=1_900_000,
            financing_percentage=0.75,
            interest_rate=0.045,
            loan_term=25,
        ),
        assumptions=Assumptions(
            investment_term=7,
            annual_apartment_price_growth=0.065,
            annual_rent_percentage=0.023,
            rent_increase_delta=1,
            annual_market_return=0.075,
            buy_expenses=100_000,
            new_apartment_current_value=3_150_000,
        ),
    )
    print(estimation)


if __name__ == "__main__":
    main()
