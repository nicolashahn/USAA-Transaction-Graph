#!/usr/bin/python3

# Graph transactions from USAA account to monitor spending
# Nicolas Hahn
# 2016.3.17

import csv
import sys
import matplotlib.pyplot as plt

class Transaction:
    '''store necessary information for a single transaction'''
    
    def __init__(self,date,name,amount):
        self.date = date
        self.name = name
        self.amount = float(amount.replace('--',''))

    def __str__(self):
        return self.date+', '+self.name+', '+str(self.amount)


def graph_transactions(transaction_list, date_total=0):
    '''
    take a list of transaction objects, create a graph
    date_total = starting balance of account
    '''
    
    transaction_list_sorted = sorted(transaction_list, key=lambda x: x.date)
    date_totals = []
    curr_date = transaction_list_sorted[0].date
    # the number of dates after the first date
    t_plus_date = 0
    for transaction in transaction_list_sorted:
        if transaction.date == curr_date:
            date_total += transaction.amount
        else:
            date_totals.append((curr_date, date_total, t_plus_date))
            curr_date = transaction.date
            t_plus_date += 1
            date_total += transaction.amount
    t_plus_dates = [date_total[2] for date_total in date_totals]
    amounts = [date_total[1] for date_total in date_totals]
    plt.plot(t_plus_dates, amounts)
    plt.show()


def main(transactions_csv=sys.argv[1]):
    with open(transactions_csv, 'r') as file:
        csv_lines = csv.reader(file.readlines())
        transactions = [Transaction(line[2],line[4],line[6]) for line in csv_lines if len(line) == 7]
    graph_transactions(transactions)


if __name__ == "__main__":
    main()
