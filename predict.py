# import libs
from time import sleep
from numpy import array

# import files
from kalman import KalmanFilter
from utils import LoadTransactions, Transactions, GetLiveStockData, GetDateTime, WriteTransactions
from configure import STOCKS

Transaction = Transactions()


def buy(transactions, stock, history):
    # add the object o to the bought and onhold lists
    history["stock"] = stock
    transactions['bought'].append(history)
    transactions['onhold'][stock] = history
    if ((Transaction.amount)/len(STOCKS)) > history["bought_at"]:
        Transaction.Withdrawn(history["bought_at"])
        print(
            f"bought {stock} at {history['bought_at']} at {GetDateTime()['time']}")
    else:
        print(
            f"Don't have enough money to buy {stock} at {history['bought_at']} at {GetDateTime()['time']}")
    return transactions


def sell(transactions, stock, sold_at):
    history = transactions['onhold'][stock]
    history["sold_at"] = sold_at
    history["stock"] = stock
    # add the object to sold list
    transactions['sold'].append(history)
    # remove the object o from onhold list
    transactions['onhold'].pop(stock)
    # the money for selling the stock
    Transaction.Debit(history['sold_at'])
    print(f"sold {stock} at {history['sold_at']} at {GetDateTime()['time']}")
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
        stock_data[stock] = KalmanFilter(closePrice=stock_price[0], dt=300)

    while(True):
        for stock in STOCKS:
            # get the live price of the stock
            price = array([GetLiveStockData(stock)], dtype="float64")
            price = price[0]

            if transactions['onhold'].get(stock) != None:
                # update the kalman filter to the current state
                stock_data[stock].update(price)
                # predict the next state
                prediction = stock_data[stock].predict()[0][0]
                # the bought at price for the stock
                boughtAt = transactions['onhold'][stock]["bought_at"]

                if ((prediction < price) and (boughtAt < prediction)) or ((boughtAt > prediction) and (prediction < price)):
                    transactions = sell(transactions, stock, price)
                    WriteTransactions(transactions)

            else:
                # update the kalman filter to current state
                stock_data[stock].update(price)
                # make the predictions using the kalman filter
                predicted_price = stock_data[stock].predict()[0][0]

                # for first 10 iterations we will reduce the noise in kalman filterr for better predictions
                if (predicted_price - price) > 0 and iterations > 10:

                    # sold_at -1 means it is not sold yet or we don't know the selling price
                    transactions = buy(transactions, stock, {
                        "bought_at": price,
                        "sold_at": -1
                    })

        # we will wait for 5 minutes
        sleep(300)
        iterations += 1
        print(f"Amount {Transaction.amount} at {GetDateTime()['time']}")


if __name__ == "__main__":
    main()
