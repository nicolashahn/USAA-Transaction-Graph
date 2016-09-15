#!/usr/local/bin/python3

# Graph transactions from USAA account to monitor spending
# Nicolas Hahn
# 2016.3.17

# Usage: python graph_transactions.py <transactions.csv> <current_balance>

import csv
import sys
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

# default how many days back to calculate balance in get_period_balance()
period = 7
# current balance after all transactions, used to show accurate account balances for all transactions
curr_balance = 0

class Transaction:
    '''store necessary information for a single transaction'''
    
    def __init__(self, raw_date, name, amount):
        month, day, year = tuple(raw_date.split('/'))
        self.date = datetime.date(int(year), int(month), int(day))
        self.name = name
        self.amount = float(amount.replace('--',''))

    def __str__(self):
        return str(self.date)+', '+self.name+', '+str(self.amount)


def get_period_balance(transaction_list, period=period):
    '''takes transaction list and list of dates in a period and calculates balance'''
   
    #TODO: this currently uses the current date, have it use the last date in the transaction list
    today = datetime.datetime.now()
    period_dates = []
    for day in range(1,period+1):
        date = today - datetime.timedelta(day)
        period_dates.append(datetime.date(date.year, date.month, date.day))
    balance = 0
    for transaction in transaction_list:
        if transaction.date in period_dates:
            balance -= transaction.amount
    return balance


def graph_transactions(transaction_list, curr_balance=0):
    '''
    take a list of transaction objects, create a graph
    curr_date_total = current balance of account to date
    '''
    
    transaction_list_sorted = sorted(transaction_list, key=lambda x: x.date)
    date_totals = []
    date_total = 0
    curr_date = transaction_list_sorted[0].date
    for transaction in transaction_list_sorted:
        date_total += transaction.amount
        if transaction.date != curr_date:
            date_totals.append((curr_date, date_total))
            curr_date = transaction.date
    # difference between actual current balance and 'start from 0' balance
    curr_diff = curr_balance - date_total
    fixed_date_totals = [(dt[0],dt[1]+curr_diff) for dt in date_totals]
    dates = [dt[0] for dt in fixed_date_totals]
    amounts = [dt[1] for dt in fixed_date_totals]
    plt.rcParams["figure.figsize"] = (14,8)
    plt.plot(dates, amounts)
    plt.show()


def main(transactions_csv, curr_balance, period):

    with open(transactions_csv, 'r') as file:
        csv_lines = csv.reader(file.readlines())
        transactions = [Transaction(line[2],line[4],line[6]) for line in csv_lines if len(line) == 7]
    print('Your net balance is $'+str(get_period_balance(transactions, period))+
          ' for the last '+str(period)+' days.')
    graph_transactions(transactions, curr_balance)


if __name__ == "__main__":

    transactions_csv = sys.argv[1]
    if len(sys.argv) >= 3: curr_balance = float(sys.argv[2])
    if len(sys.argv) >= 4: period = int(sys.argv[3])
    main(transactions_csv, curr_balance, period)
