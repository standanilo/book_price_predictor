import numpy as np
import pandas as pd

class StandardScaler:
    def __init__(self):
        self.mean_ = None
        self.scale_ = None
    
    def fit(self, X):
        X = np.array(X)
        self.mean_ = X.mean(axis=0)
        self.scale_ = X.std(axis=0, ddof=0)
    
    def transform(self, X):
        X = np.array(X)
        return (X - self.mean_) / self.scale_
    
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    
    def inverse_transform(self, X_scaled):
        X_scaled = np.array(X_scaled)
        return X_scaled * self.scale_ + self.mean_