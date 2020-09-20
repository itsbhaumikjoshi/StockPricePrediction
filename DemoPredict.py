# import libs
import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import requests

# import files
from kalman import KalmanFilter
from configure import YOUR_API_KEY, DEMO_STOCK

def GetStockData(stock=DEMO_STOCK):
    try:
        # Get the stock history
        response = requests.get(
            f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=5min&outputsize=compact&apikey={YOUR_API_KEY}')

        if response.status_code == 200:
            return response.json()
        sys.exit(f"Response for the {stock} returned with status code: {response.status_code}")
    except:
        sys.exit(f'Error fetching data for {stock}')
    return None

def Demo(data):
    try:
        # check if the file exists in the directory named as demo.json
        if os.path.exists("demo.json"):
            # if yes open the file and read the data
            with open('demo.json') as file:
                data = json.load(file)
        else:
            # store the data into a file so that we don't have to request for the data again
            with open('demo.json', 'w') as file:
                json.dump(data, file, indent=4)
    except:
        sys.exit("There was an Error loading the data")

    # temp list to store the data
    m = []

    for i in data['Time Series (5min)'].values():
        t = np.array([float(i['4. close'])], dtype='float64')
        m.append(t[0])

    # as the data is store in desending order we will reverse it
    measurements = m[::-1]

    # initialise the kalman filter
    kalman = KalmanFilter(closePrice=measurements[0], dt=300)

    # to store the predictions
    predictions = []

    # to predict the next state store it and update the filter
    for value in measurements:
        predictions.append(kalman.predict()[0][0])
        kalman.update(value)

    # calculate the r2 score
    coefficient_of_dermination = r2_score(measurements, predictions)
    print(f'R2 score of the filter {coefficient_of_dermination}')

    plt.figure(figsize=(10,5))
    plt.plot(measurements, label='measurements', marker='*', color="red")
    plt.plot(predictions, label='prediction', marker=".", color="blue")
    plt.suptitle("Kalman filter predictions")
    plt.title("Intially the filter prediction has noise so prediction can divert")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    data = GetStockData()
    Demo(data)
