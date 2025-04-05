import sklearn.metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from createDataset import CreateDataSet
import pandas as pd

class f1Model():
    def __init__(self, x, y):
        xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.3)
        self.model = self.trainModel(xTrain, yTrain)

    def trainModel(self, xTrain, yTrain):
        model = RandomForestClassifier()
        print(f"Training Model")
        model.fit(xTrain, yTrain)
        return model

    def evaluateModel(self, model, xTest, yTest):
        predictions = model.predict(xTest)
        precision, recall, f1Score, _ = sklearn.metrics.precision_recall_fscore_support(
            y_true = yTest, y_pred=predictions)

        print(f"Recall score: {recall}")
        print(f"F1 Score: {f1Score}")
        print(f"Precision: {precision}")

    def predictRaceStrategy(self, model, GP, year, data=None):
        if data:
            print(self.model.predict(data))

        else:
            CreateDataSet([year], GP)
            dataSet = pd.read_csv(f"{GP}{[year]}.csv")
            dataSet = dataSet.drop(columns=["Compound"])

            print(self.model.predict(dataSet))

