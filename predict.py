# import libs
from time import sleep

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

    while(True):
        # checking if the market is closed or not
        if CURRENT_TIME < OPEN_TIME or CURRENT_TIME > CLOSE_TIME:
            print('Stock market is closed!')
            break

        for stock in STOCKS:
            # get the info for the stock
            data = GetStockData(stock)

            # get the kalman filter
            kalman = KalmanFilter(closePrice=20.0, dt=300)

            # estimate the price using the kalman filter
            # decide whether to buy it or not
            # transactions = buy(transactions, data)
            # make the respective changes to the transactions dict
            # write the transaction dict to the JSON file if they have been changed
            WriteTransactions(transactions)
            # we are waiting for 300 seconds or 5 minutes to request again
            sleep(300/len(STOCKS))
            # checking if the market is closed or not
            if CURRENT_TIME < OPEN_TIME or CURRENT_TIME > CLOSE_TIME:
                print('Stock market is closed!')
                break


if __name__ == "__main__":
    main()
