import numpy as np

def softmax(z):
    exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)

class LogisticRegression:
    def __init__(self, lr=0.01, num_iterations=1000):
        self.lr = lr
        self.num_iterations = num_iterations
        self.class_labels = None
        self.weights = None
        self.w0 = None

    def fit(self, X, Y, class_labels):
        n_samples, n_features = X.shape
        self.class_labels = class_labels
        n_classes = len(class_labels)

        class_mapping = {label: idx for idx, label in enumerate(class_labels)}
        Y_mapped = np.array([class_mapping[label] for label in Y])

        self.weights = np.random.randn(n_features, n_classes) * self.lr
        self.w0 = np.zeros((1, n_classes))

        for _ in range(self.num_iterations):
            y_lin_pred = np.dot(X, self.weights) + self.w0
            y_log_pred = softmax(y_lin_pred)
            
            Y_one_hot = np.eye(y_log_pred.shape[1])[Y_mapped]
            dZ = y_log_pred - Y_one_hot
            
            dw = (1/n_samples) * np.dot(X.T, dZ)
            db = (1/n_samples) * np.sum(dZ, axis=0, keepdims=True)
            self.weights = self.weights - self.lr * dw - self.weights * self.lr * 0.1 * (1/n_samples)
            self.w0 = self.w0 - self.lr * db


    def predict(self, X):
        y_lin_pred = np.dot(X, self.weights) + self.w0
        y_pred = softmax(y_lin_pred)
        predictions_mapped = np.argmax(y_pred, axis=1)

        index_to_class = {idx: label for idx, label in enumerate(self.class_labels)}
        predictions = np.array([index_to_class[idx] for idx in predictions_mapped])
        
        return predictions
