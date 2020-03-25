import json
import datetime

# base to write an empty JSON file
base = {
    "bought":[],
    "onhold":[],
    "sold":[]
}
# watch any five stocks
watch = []

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
        # create a json data file for today and write the base data to it
        with open(f"{getDateTime()['date']}.json", "w") as transaction:
            transaction.write(json.dumps(base, indent=4))
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