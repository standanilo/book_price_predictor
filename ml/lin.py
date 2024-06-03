import numpy as np


class LinearRegression:
    
    def __init__(self, lr=0.001, n_iters=1000):
        self.lr = lr
        self.n_iters = n_iters
        self.weights = None
        self.w0 = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.w0 = 0

        for _ in range(self.n_iters):
            y_pred = np.dot(X, self.weights) + self.w0

            dw = (1/n_samples) * np.dot(X.T, (y_pred-y)) * 2
            dw0 = (1/n_samples) * np.sum(y_pred-y) * 2

            self.weights = self.weights - self.lr * dw
            self.w0 = self.w0 - self.lr * dw0

    def predict(self, X):
        return np.dot(X, self.weights) + self.w0
    
    def score(self, y_pred, y_test):
        ts = np.sum((y_test - np.mean(y_test)) ** 2)
        rs = np.sum((y_test - y_pred) ** 2)
        return 1 - (rs / ts)


def train_test_split(X, y, test_size=0.25, random_state=None, shuffle=True):    
    indices = list(range(X.shape[0]))
    num_training_indices = int((1 - test_size) * X.shape[0])
    if shuffle:
        np.random.seed(random_state)
        np.random.shuffle(indices)
    train_indices = indices[:num_training_indices]
    test_indices = indices[num_training_indices:]

    X_train, X_test = X.iloc[train_indices], X.iloc[test_indices]
    y_train, y_test = y.iloc[train_indices], y.iloc[test_indices]
    return X_train, X_test, y_train, y_test

def mse(y_test, predictions):
    return np.mean((y_test-predictions)**2)
