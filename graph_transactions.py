#!/usr/bin/python3

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
PERIOD = 7

class Transaction:
    '''store necessary information for a single transaction'''
    
    def __init__(self, raw_date, name, amount):
        month, day, year = tuple(raw_date.split('/'))
        self.date = datetime.date(int(year), int(month), int(day))
        self.name = name
        self.amount = float(amount.replace('--',''))

    def __str__(self):
        return str(self.date)+', '+self.name+', '+str(self.amount)


def get_period_balance(transaction_list, period=PERIOD):
    '''takes transaction list and list of dates in a period and calculates balance'''
    
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

def graph_transactions(transaction_list, date_total=0):
    '''
    take a list of transaction objects, create a graph
    date_total = current balance of account to date
    '''
    
    transaction_list_sorted = sorted(transaction_list, key=lambda x: x.date)
    date_totals = []
    curr_date = transaction_list_sorted[0].date
    for transaction in transaction_list_sorted:
        if transaction.date == curr_date:
            date_total += transaction.amount
        else:
            date_totals.append((curr_date, date_total))
            curr_date = transaction.date
            date_total += transaction.amount
    dates = [date_total[0] for date_total in date_totals]
    amounts = [date_total[1] for date_total in date_totals]
    plt.rcParams["figure.figsize"] = (14,8)
    plt.plot(dates, amounts)
    plt.show()

def main(transactions_csv, curr_balance):
    with open(transactions_csv, 'r') as file:
        csv_lines = csv.reader(file.readlines())
        transactions = [Transaction(line[2],line[4],line[6]) for line in csv_lines if len(line) == 7]
    print('Your net balance is $'+str(get_period_balance(transactions, PERIOD))+
          ' for the last '+str(PERIOD)+' days.')
    graph_transactions(transactions, curr_balance)

if __name__ == "__main__":
    transactions_csv = sys.argv[1]
    if len(sys.argv) == 3: curr_balance = float(sys.argv[2])
    else: curr_balance = 0
    main(transactions_csv, curr_balance)

