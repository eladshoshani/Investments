# Apartment Investment Estimator

## Overview

This project provides utilities to estimate the return on investment (ROI) for various types of investments, with a
focus on real estate investments. The primary utility provided is an estimation tool for buying an apartment, renting it
out, and then selling it after a few years. The module calculates the monthly cashflows, missed market gains, and the
final capital after selling the apartment, ultimately computing the average annual return on the investment.

**Note: This project is a work in progress and is not yet complete, don't take it too seriously - I wrote it so I won't
have to do the math myself manually.**

## Features

- **Monthly Cashflows Calculation**: Computes the monthly cashflows considering the rent income and mortgage payments.
- **Missed Market Gains Calculation**: Estimates the potential gains missed from negative cashflows that could have been
  invested in the market.
- **Final Capital Calculation**: Calculates the remaining capital after selling the apartment, considering the mortgage
  balance, selling expenses, and missed market gains.
- **Average Annual Return Calculation**: Computes the average annual return on the investment based on the initial and
  final capital.

## Assumptions and Notes

- Tax implications and inflation are not considered.
- The apartment is assumed to be rented throughout the investment term.
- The apartment is assumed to be sold at the end of the investment term.
- Rent is assumed to increase every few years.
- Mortgage payments are assumed to be constant and paid in equal monthly installments.
- Mortgage interest rate is assumed to remain constant.

## Getting Started

### Prerequisites

- Python 3.7+
- `mortgage` library
- `pyyaml` library

Install the required libraries using pip:

```bash
pip install -r requirements.txt
```

### Usage

Just run the script `apartment.py` with the modified data for your own investment/calculations.

```bash
python apartment.py
```

Example output:

```text
Average annual return: 20.60%
Initial capital: 650000.0
Final capital: 2411485.057962168
Buy price: 1900000
Sell price: 3834257.1604279694
Investment term: 7 years
Interest paid on mortgage: 344510.1627375477
Monthly (distinct) cashflows:
[-2625.8, -2069.5999999999995, -1444.6536799999985, -742.4639948479971]
Total loss from cashflows: 213718.33039330796
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss improvements or bug fixes.