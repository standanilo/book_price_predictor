import numpy as np

def sigmoid(z):
    return 1/(1+np.exp(-z))

class LogisticRegression():

    def __init__(self, lr=0.01, num_iterations=1000):
        self.lr = lr
        self.num_iterations = num_iterations
        self.weights = None
        self.w0 = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.w0 = 0

        for _ in range(self.num_iterations):
            y_lin_pred = np.dot(X, self.weights) + self.w0
            y_log_pred = sigmoid(y_lin_pred)

            dw = (1/n_samples) * np.dot(X.T, (np.array(y_log_pred) - y))
            dw0 = (1/n_samples) * np.sum(y_log_pred-y)

            self.weights = self.weights - self.lr*dw - self.weights * self.lr * 0.1 * (1/n_samples)
            self.w0 = self.w0 - self.lr*dw0

    def predict(self, X):
        y_lin_pred = np.dot(X, self.weights) + self.w0
        y_pred = sigmoid(y_lin_pred)
        class_pred = [0 if y<=0.5 else 1 for y in y_pred]
        return class_pred
    

class OneVsOneLogisticRegression:
    def __init__(self):
        self.models = {}

    def fit(self, X, y):
        classes = np.unique(y)
        for i in range(len(classes)):
            for j in range(i + 1, len(classes)):
                class1 = classes[i]
                class2 = classes[j]
                X_pair, y_pair = self._extract_pairwise_data(X, y, class1, class2)
                model = LogisticRegression()
                model.fit(X_pair, y_pair)
                self.models[(class1, class2)] = model

    def predict(self, X):
        votes = np.zeros((X.shape[0], len(self.models) * 2))
        class_list = []

        for idx, (pair, model) in enumerate(self.models.items()):
            class1, class2 = pair
            class_list.extend([class1, class2])
            pred = model.predict(X)
            for i in range(X.shape[0]):
                if pred[i] == 1:
                    votes[i, idx * 2] += 1
                else:
                    votes[i, idx * 2 + 1] += 1

        final_predictions = []
        class_list = np.unique(class_list)

        for i in range(X.shape[0]):
            class_votes = {cls: 0 for cls in class_list}
            for j in range(len(self.models)):
                if votes[i, j * 2] > votes[i, j * 2 + 1]:
                    class_votes[list(self.models.keys())[j][0]] += 1
                else:
                    class_votes[list(self.models.keys())[j][1]] += 1

            sorted_votes = sorted(class_votes.items(), key=lambda x: x[1], reverse=True)
            final_predictions.append(sorted_votes[0][0])

        return np.array(final_predictions)

    def _extract_pairwise_data(self, X, y, class1, class2):
        mask = (y == class1) | (y == class2)
        X_pair = X[mask]
        y_pair = y[mask]
        y_pair = np.where(y_pair == class1, 1, 0)
        return X_pair, y_pair
