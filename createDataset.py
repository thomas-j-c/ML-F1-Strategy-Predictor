import fastf1 as f1
import numpy as np
import pandas as pd

class CreateDataSet():
    def __init__(self, years, GP):
        data = pd.DataFrame()
        for year in years:
            print(f"Getting Data for Year {year}")
            session = f1.get_session(year, GP, "R")
            session.load()
            data = pd.concat([data, self.getData(session)], axis=0)

        data.to_csv(f"{GP}{years}.csv")

    def getLapTimesAndCompound(self, session):
        times = []
        for driver in pd.unique(session.laps["Driver"]):
            driverSession = session.laps.pick_drivers(driver)
            lapTime = driverSession["LapTime"]
            tyre = driverSession["Compound"]
            count = 0
            for lap, tyreComp in zip(lapTime, tyre):
                lapDict = {"Driver": driver, "Lap": count,
                           "Time": lap.total_seconds(), "Compound": tyreComp}

                if pd.notnull(lap):
                    times.append(lapDict)

                count += 1

        return times

    def getBestTimesForLap(self, session, lap):
        allLaps = self.getLapTimesAndCompound(session)

        timesForLap = []
        compounds = []

        for i in allLaps:
            if i["Lap"] == lap:
                timesForLap.append(i["Time"])
                compounds.append(i["Compound"])
        if not len(timesForLap) == 0:
            bestLap = min(timesForLap)
            bestLapIndex = [i for i, j in enumerate(timesForLap) if j == bestLap][0]
            return bestLap, compounds[bestLapIndex]

        else:
            return 0, 0

    def getWeatherDataForLap(self, session, lapNo):
        allLaps = session.laps
        return allLaps.iloc[lapNo].get_weather_data()

    def getData(self, session):
        numLaps = session.total_laps
        data = {}

        for i in range(1, numLaps):
            bestlap, bestCompound = self.getBestTimesForLap(session, i)
            weather = self.getWeatherDataForLap(session, i)

            if bestlap == 0:
                continue

            data[i] = {"Time": bestlap, "Compound": bestCompound,
                         "AirTemp":weather["AirTemp"], "TrackTemp": weather["TrackTemp"],
                         "Pressure": weather["Pressure"], "Rain": weather["Rainfall"],
                         "WindSpd": weather["WindSpeed"], "WindDir": weather["WindDirection"]}

        df = pd.DataFrame.from_dict(data, orient="index")
        return df

if __name__ == '__main__':
    create = CreateDataSet([2022,2023, 2024], "Australian Grand Prix")
