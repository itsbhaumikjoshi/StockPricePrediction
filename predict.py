# import libs
from time import sleep

# import files
from kalman import KalmanFilter
from utils import LoadTransactions, WriteTransactions, GetStockData

OPEN_TIME = ''
CLOSE_TIME = ''


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
    # watch your stocks
    stock = ""
    # keep the track the current day transactions
    transactions = LoadTransactions()
    while(True):
        # current state
        currentState = None

        # assuming Adjusted Close at 1, it is nothing but the price closed a day before / price close for today
        adjClose = 1

        # get the info for the stock
        data = GetStockData(stock)
        # get the kalman filter
        kalman = KalmanFilter(closePrice=20.0, dt=300)
        # estimate the price using the kalman filter
        # decide whether to buy it or not
        transactions = buy(transactions, data)
        # make the respective changes to the transactions dict
        # write the transaction dict to the JSON file if they have been changed
        WriteTransactions(transactions)
        # we are waiting for 300 seconds or 5 minutes to request again
        sleep(5*60)


if __name__ == "__main__":
    main()
