import numpy as np

class LogisticRegression:
    def __init__(self, lr=0.01, num_iterations=1000):
        self.lr = lr
        self.num_iterations = num_iterations
        self.class_labels = None

    def softmax(self, z):
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def fit(self, X, Y, class_labels):
        n_features = X.shape[1]
        self.class_labels = class_labels
        n_classes = len(class_labels)

        class_mapping = {label: idx for idx, label in enumerate(class_labels)}
        Y_mapped = np.array([class_mapping[label] for label in Y])

        self.weights = np.random.randn(n_features, n_classes) * 0.01
        self.w0 = np.zeros((1, n_classes))

        for _ in range(self.num_iterations):
            Z = np.dot(X, self.weights) + self.w0
            A = self.softmax(Z)
            m = X.shape[0]
            Y_one_hot = np.eye(A.shape[1])[Y_mapped]
            dZ = A - Y_one_hot
            dweights = np.dot(X.T, dZ) / m
            db = np.sum(dZ, axis=0, keepdims=True) / m
            self.weights = self.weights - self.lr * dweights
            self.w0 = self.w0 - self.lr * db


    def predict(self, X):
        Z = np.dot(X, self.weights) + self.w0
        A = self.softmax(Z)
        predictions_mapped = np.argmax(A, axis=1)

        index_to_class = {idx: label for idx, label in enumerate(self.class_labels)}
        predictions = np.array([index_to_class[idx] for idx in predictions_mapped])
        
        return predictions
