import pandas as pd
from model import f1Model

if __name__ == '__main__':
    data = pd.read_csv("Australian Grand Prix[2022, 2023, 2024].csv")

    y = data["Compound"]
    x = data.drop(columns=["Compound"])

    model = f1Model(x, y)
    model.predictRaceStrategy(model, "Australian Grand Prix", 2025)
