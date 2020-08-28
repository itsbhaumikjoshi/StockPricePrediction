from numpy import array, dot, eye
from numpy.linalg import inv


class KalmanFilter:
    def __init__(self, closePrice, dt):
        # initializing ground parameters
        self.dt = dt # number of seconds / time scale
        self.f = array([[1, self.dt], [0, 1]])
        self.x = array([[closePrice], [0]])
        self.p = eye(self.x.shape[0])
        self.h = array([[1, 0],[0, 0]])
        self.r = eye(self.x.shape[0])

    # Predicting the next state / price
    def predict(self):
        # x = f*x
        self.x = dot(self.f, self.x)
        # p = (f*p)*(f transpose) + identity
        self.p = dot(dot(self.f, self.p), self.f.T) + eye(self.x.shape[0])
        return self.x

    # updating the parameters
    def update(self, originalPrice):
        # y = orignal - h*x
        self.y = originalPrice - dot(self.h, self.x)
        # s = h * (p*(h transpose)) + r
        s = dot(self.h, dot(self.p, self.h.T)) + self.r
        # k = p*(h transpose) * (s^-1)
        self.k = dot(dot(self.p, self.h.T), inv(s))
        # x = x + k*y
        self.x = self.x + dot(self.k, self.y)
        # p = (identity - (k*h)) * p
        self.p = dot((eye(self.x.shape[0]) - dot(self.k, self.h)), self.p)

    def getParameters(self):
        return f"Kalman Gian: {self.k}, closedPrice: {self.x}"