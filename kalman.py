import numpy as np


class KalmanFilter:
    def __init__(self, x: float):
        self.x = np.array([x, 0])
        self.p = np.eye(self.x.shape[0])
        self.dt = 300 # number of seconds
        self.f = np.array([[1, self.dt], [0, 1]])
        self.g = np.array([[1/2*(self.dt**2)],[self.dt]])
        self.h = np.array([[1, 0]])

    def predict(self):
        # x = fx
        # p = fp(f transpose) + g(g transpose)
        self.x = self.f.dot(self.x)
        self.p = self.f.dot(self.p).dot(self.f.T) + self.g.dot(self.g.T)

    def update(self, val, variance):
        # y = z - Hx
        # s = hp(h transpose) + r
        # k = p(h transpose) * (s inverse)
        # x = x + ky
        # p = (i - kh) * p
        self.y = np.array([val]) - self.h.dot(self.x)
        s = self.h.dot(self.p).dot(self.h.T) + np.array([variance])
        self.k = self.p.dot(self.h.T).dot(np.linalg.inv(s))
        # Calculate Kalman gain (3x1)

        # Update x and P
        self.x = self.x + self.k.dot(self.y)
        self.P = (np.eye(2) - self.k.dot(self.h)).dot(self.p)
    
    def get_covariance_matrix(self):
        return self.p

    def get_pred_value(self):
        return self.x[0]