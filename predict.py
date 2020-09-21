# import libs
import sys
from time import sleep
from datetime import datetime
from numpy import array

# import files
from kalman import KalmanFilter
from utils import LoadTransactions, WriteTransactions, GetLiveStockData
from configure import *

def buy(transactions, o):
    # add the object o to the bought and onhold lists
    transactions['bought'].append(o)
    transactions['onhold'].append(o)
    print(f"bought {o}")
    return transactions


def sell(transactions, o):
    # add the object to sold list
    transactions['sold'].append(o)
    # remove the object o from onhold list
    for hold in transactions['onhold']:
        if(hold['id'] == o['id']):
            transactions['onhold'].pop(o['id'])
    print(f"sold {o}")
    return transactions


def main():    
    # keep the track the current day transactions
    transactions = LoadTransactions()

    # initiate kalman filter for all STOCKS and store the previous closing prices
    stock_data = dict()

    # For first 10 iterations we won't predict and let the kalman filter to reduce the noise
    # But we will update the kalman filter
    iterations = 0

    for stock in STOCKS:
        stock_price = array([GetLiveStockData(stock)], dtype='float64')
        # initial Close price = 0
        stock_data[stock] = {
            'kalman' : KalmanFilter(closePrice=stock_price[0], dt=300),
            'adjClose' : stock_price[0]
        }

    while(True):
        for stock in STOCKS:
            # get the live price of the stock
            price = array([GetLiveStockData(stock)], dtype="float64")
            price = price[0]

            # make the predictions using the kalman filter
            predicted_price = stock_data[stock].kalman.predict()[0][0]

            # last state
            last_price = stock_data[stock]['adjClose']

            # for first 10 iterations we will reduce the noise in kalman filterr for better predictions
            if (predicted_price - last_price) > 0 and iterations > 10:
                pass

            # update the kalman filter
            stock_data[stock].kalman.update(price)

            # current price will be the last price for the next iteration
            stock_data[stock]['adjClose'] = price


        # we will wait 5 minutes for the price to change
        sleep(300)
        iterations += 1


if __name__ == "__main__":
    main()
