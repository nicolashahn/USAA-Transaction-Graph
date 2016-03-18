#!/usr/bin/python3

# Graph transactions from USAA account to monitor spending
# Nicolas Hahn
# 2016.3.17

import csv
import sys
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

class Transaction:
    '''store necessary information for a single transaction'''
    
    def __init__(self,raw_date,name,amount):
        month, day, year = tuple(raw_date.split('/'))
        self.date = datetime.date(int(year), int(month), int(day))
        self.name = name
        self.amount = float(amount.replace('--',''))

    def __str__(self):
        return str(self.date)+', '+self.name+', '+str(self.amount)


def graph_transactions(transaction_list, date_total=0):
    '''
    take a list of transaction objects, create a graph
    date_total = current balance of account
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
    plt.plot(dates, amounts)
    plt.show()


def main(transactions_csv=sys.argv[1]):
    with open(transactions_csv, 'r') as file:
        csv_lines = csv.reader(file.readlines())
        transactions = [Transaction(line[2],line[4],line[6]) for line in csv_lines if len(line) == 7]
    graph_transactions(transactions)


if __name__ == "__main__":
    main()
