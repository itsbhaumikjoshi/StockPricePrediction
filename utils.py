import sys
import datetime
import json
import requests
from bs4 import BeautifulSoup

from configure import DEMO_STOCK

base_case = {
    "bought": [],
    "onhold": [],
    "sold": []
}

# returns date and time
def GetDateTime(s='today'):
    today = datetime.datetime.today()
    if s == 'yesterday':
        date = (today - datetime.timedelta(days=1)).strftime("%d-%m-%Y")
        time = (today - datetime.timedelta(days=1)).strftime("%H:%M:%S")
    elif s == 'tomorrow':
        date = (today + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
        time = (today + datetime.timedelta(days=1)).strftime("%H:%M:%S")
    elif s == 'today':
        date = datetime.datetime.today().strftime("%d-%m-%Y")
        time = datetime.datetime.today().strftime("%H:%M:%S")
    return {
        "date": date,
        "time": time
    }

# Load current day transactions
def LoadTransactions():
    try:
        # try reading today's json data file
        with open(f"{GetDateTime()['date']}.json", "r") as transaction:
            return json.load(transaction)
    except:
        # create a json file for today
        open(f'{GetDateTime()}.json', 'w').close()
        try:
            # check the yesterday's json data file, if there are any stocks onhold? if there are then return the onhold transactions to today
            with open(f"{GetDateTime('yesterday')['date']}.json", "r") as transaction:
                if(len(json.load(transaction)['onhold'])):
                    holders = {
                        "bought": [],
                        "onhold": json.load(transaction)['onhold'],
                        "sold": []
                    }
                    # also write onhold stocks to the current file
                    WriteTransactions(holders)
                    return holders
        except:
            # if there is no yesterday's json data file then pass
            pass

    WriteTransactions(base_case)
    return base_case

# write to transactions JSON file
def WriteTransactions(transactions):
    try:
        # dump the transactions to today's file
        with open(f"{GetDateTime()['date']}.json", "w") as transaction:
            transaction.write(json.dumps(transactions, indent=4))
    except:
        sys.exit(f"Unable to write to {GetDateTime()}.json file")


def GetLiveStockData(stock=DEMO_STOCK):
    try:
        URL = f'https://in.finance.yahoo.com/quote/{stock}'
        response = requests.get(URL)
        if response.status_code is 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find("div", {"class": "D(ib) Mend(20px)"})
            stock_price = content.find(
                "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
            market_status = content.find("span", {"data-reactid": "35"}).text
            if "open" in market_status:
                return float(stock_price)
            else:
                return None
        else:
            sys.exit(
                f"Response for the {stock} returned with status code: {response.status_code}")
    except:
        sys.exit(f"Error fetching data for {stock}")
    return None
