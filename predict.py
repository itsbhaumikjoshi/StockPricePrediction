# import libs
from time import sleep
from datetime import datetime
from numpy import array
# import files
from kalman import KalmanFilter
from utils import LoadTransactions, WriteTransactions, GetStockData
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
        # initial Close price = 0
        stock_data[stock] = {
            'kalman' : KalmanFilter(closePrice=0, dt=300),
            'adjClose' : 0
        }

    while(True):
        # calculating current time
        current_time = datetime.now().strftime("%H:%M:%S")
        # checking if the market is closed or not
        if current_time < OPEN_TIME or current_time > CLOSE_TIME:
            print('Stock market is closed!')
            break

        for stock in STOCKS:
            # get the info for the stock
            data = GetStockData(stock)

            open_price = list(data.values())[0]['1. open']
            close_price = list(data.values())[0]['4. close']

            open_price = array([float(open_price)], dtype='float64')[0]
            close_price = array([float(close_price)], dtype='float64')[0]

            # estimate the price using the kalman filter
            predicted = stock_data[stock]['kalman'].predict()[0][0]
            stock_data[stock]['kalman'].update(close_price)

            if iterations > 10:
                pass
            
            # updating the adjPrice
            stock_data[stock]['adjClose'] = close_price 
            # decide whether to buy it or not
            # transactions = buy(transactions, data)
            # make the respective changes to the transactions dict
            # write the transaction dict to the JSON file if they have been changed
            WriteTransactions(transactions)
            # we are waiting for 300 seconds or 5 minutes to request again
            sleep(300/len(STOCKS))
            # calculating current time
            current_time = datetime.now().strftime("%H:%M:%S")
            # checking if the market is closed or not
            if current_time < OPEN_TIME or current_time > CLOSE_TIME:
                print('Stock market is closed!')
                break

        iterations += 1


if __name__ == "__main__":
    main()
