#!/anaconda3/bin/python

"""
  Input values  annualInterestRate , monthlyPaymentRate  , balance (initial) is updated every month
"""
annualInterestRate = 0.2
monthlyPaymentRate = 0.04
balance = 42

def monthlyBalance(balance,annualInterestRate,monthlyPaymentRate):
    """
    Monthly interest rate= (Annual interest rate) / 12.0
    Minimum monthly payment = (Minimum monthly payment rate) x (Previous balance)
    Monthly unpaid balance = (Previous balance) - (Minimum monthly payment)
    Updated balance each month = (Monthly unpaid balance) + (Monthly interest rate x Monthly unpaid balance)
    """
    balance_start_month = balance
    monthlyPayment = balance_start_month * monthlyPaymentRate
    balance_end_month = (balance_start_month - monthlyPayment)*(1 + annualInterestRate/12 )
    return balance_end_month

for month in range (0,12):
    balance = monthlyBalance(balance,annualInterestRate,monthlyPaymentRate)
    print ("Balance end of month " , month+1 , " is : " , round(balance,2))