import requests
import json
import datetime
from time import sleep
from kalman import Kalman

# base to write an empty JSON file
base = {
    "bought":[],
    "onhold":[],
    "sold":[]
}
# watch any five stocks
stocks = []

# returns date and time
def getDateTime(s='today'):
    today = datetime.datetime.today()
    if s == 'yesterday':
        date = (today - datetime.timedelta(days = 1)).strftime("%d-%m-%Y"),
        time = (today - datetime.timedelta(days = 1)).strftime("%H:%M:%S")
    elif s == 'tomorrow':
        date = (today + datetime.timedelta(days = 1)).strftime("%d-%m-%Y"),
        time = (today + datetime.timedelta(days = 1)).strftime("%H:%M:%S")
    elif s == 'today':
        date = datetime.datetime.today().strftime("%d-%m-%Y"),
        time = datetime.datetime.today().strftime("%H:%M:%S")
    return {
            "date":date,
            "time":time
        }

def loadTransactions():
    try:
        # try reading today's json data file
        with open(f"{getDateTime()['date']}.json", "r") as transaction:
            return json.load(transaction)
    except:
        try:
            # check the yesterday's json data file, if there are any stocks onhold? if there are then return the onhold transactions to today
            with open(f"{getDateTime('yesterday')['date']}.json", "r") as transaction:
                if(len(json.load(transaction)['onhold'])):
                    return {
                        "bought":[],
                        "onhold":json.load(transaction)['onhold'],
                        "sold":[]
                    }
                return base
        except:
            # if there is no yesterday's json data file then return base dict
            return base

# keep the track the current day transactions
transactions = loadTransactions()

def buy(o):
    # add the object o to the bought and onhold lists
    transactions['bought'].append(o)
    transactions['onhold'].append(o)
    print(f"bought {o}")

def sell(o):
    # add the object to sold list
    transactions['sold'].append(o)
    # remove the object o from onhold list
    for hold in transactions['onhold']:
        if(hold['id']==o['id']):
            transactions['onhold'].pop(o['id'])
    print(f"sold {o}")

def getStockData(stock):
    try:
        YOUR_API_KEY = ''
        # get the current stock response
        response = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={YOUR_API_KEY}')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Response for the {stock} returned with status code: {response.status_code}")
            return None
    except:
        print(f'Error fetching data for {stock}')
        return None

def writeTransactions():
    # create a json data file for today and write the base data to it
    try:
        # write transactions to the file
        with open(f"{getDateTime()['date']}.json", "w") as transaction:
            transaction.write(json.dumps(transactions, indent=4))
    except:
        print('Failed to write the transactions to the file')

def main():
    for stock in stocks:
        # get the info for the stock
        data = getStockData(stock)
        if data == None:
            break
        else:
            # get the kalman filter
            kalman = Kalman()
            # estimate the price using the kalman filter
            # decide whether to buy it or not
            # make the respective changes to the transactions dict
            # write the transaction dict to the JSON file if they have been changed
            writeTransactions()
        # As we are limited only with 5 requests per minute
        sleep(12)
if __name__ == "__main__": 
    main() 