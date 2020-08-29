# import libs
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# import files
from kalman import KalmanFilter
from utils import GetStockData


def Demo():
    try:
        # check if the file exists in the directory named as demo.json
        if os.path.exists("demo.json"):
            # if yes open the file and read the data
            with open('demo.json') as file:
                data = json.load(file)
        else:
            # if not then get the data
            data = GetStockData()
            # store the data into a file so that we don't have to request for the data again
            with open('demo.json', 'w') as file:
                json.dump(data, file, indent=4)
    except:
        print("There was an Error loading the data")

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

    plt.plot(measurements, label='measurements')
    plt.plot(predictions, label='prediction')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    Demo()
