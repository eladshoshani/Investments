from dataclasses import dataclass

from mortgage import Loan


@dataclass
class Assumptions:
    annual_apartment_price_growth: float
    annual_rent_percentage: float
    rent_increase_delta: int  # Number of years between rent increases
    annual_market_return: float


@dataclass
class Mortgage:
    apartment_assessor_price_evaluation: float
    financing_percentage: float  # for example, 0.75 for 75%
    interest_rate: float  # annual interest rate (for example, 0.03 for 3%)
    loan_term: int  # number of years

    def __post_init__(self):
        self._loan = Loan(
            principal=self.loan_amount,
            interest=self.interest_rate,
            term=self.loan_term,
            currency="₪",
        )

    @property
    def loan_amount(self):
        return self.apartment_assessor_price_evaluation * self.financing_percentage

    @property
    def monthly_payment(self):
        return self._loan.monthly_payment

    def calculate_total_payment(self):
        return self.monthly_payment * self.loan_term * 12

    def calculate_balance(self, months: int):
        # get the balance of the loan after a given number of months (what left to pay, without the interest)
        return self._loan.schedule(months).balance


def get_avg_annual_return(
    apartment_price: float = 1_900_900,
    investment_term: int = 7,
    mortgage: Mortgage = Mortgage(
        apartment_assessor_price_evaluation=1_800_000,
        financing_percentage=0.75,
        interest_rate=0.04,
        loan_term=25,
    ),
    assumptions: Assumptions = Assumptions(
        annual_apartment_price_growth=0.06,
        annual_rent_percentage=0.03,
        rent_increase_delta=2,
        annual_market_return=0.075,
    ),
):
    pass
