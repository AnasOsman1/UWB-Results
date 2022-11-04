import numpy as np
from statistics import mean
import pandas as pd
import os
import glob
import shutil


def interpol(data):
    new1 = pd.DataFrame()
    print(len(data.x))
    print(data.x[0])
    for i in range(1, len(data.x), 1):
        if i < len(data.x)-1:
            nn = np.linspace(data.x[i], data.x[i+1], num=12)
            ss = np.linspace(data.y[i], data.y[i+1], num=12)
            nn = nn.tolist()
            ss = ss.tolist()
            ss.remove(data.y[i+1])
            nn.remove(data.x[i+1])
            nn = [round(num, 6) for num in nn]
            ss = [round(num, 6) for num in ss]
            new = pd.DataFrame({"x": nn, "y":  ss})
            new1 = pd.concat([new1, new])
        elif i == (len(data.x)-2):
            nn = np.linspace(data.x[i], data.x[i+1], num=12)
            ss = np.linspace(data.y[i], data.y[i+1], num=12)
            nn = nn.tolist()
            ss = ss.tolist()
            new = pd.DataFrame({"x": nn, "y":  ss})
            new1 = pd.concat([new1, new])
        else:
            break
    print("The diffrance in mean in X is: ", mean(data.x) - mean(new1.x))
    print("The diffrance in mean in Y is: ", mean(data.y) - mean(new1.y))
    return(new1)


def cast(File_Path, typ):
    path = File_Path
    directory = typ+"_trial_test"
    path2 = os.path.join(path, directory)

    # overwrite if already exists
    if os.path.exists(path2):
        print("Path already exists' Override!")
        shutil.rmtree(path2)
    os.mkdir(path2)
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    print(csv_files)
    for file in csv_files:
        a = interpol(pd.read_csv(file))
        file = file[:file.rfind('.csv')]
        a.to_csv(file+"_trial.csv")
        shutil.move(file+"_trial.csv", path2)

    print("\n End of trial, No Errors!")


File_Path = "/Users/anasosman/Downloads/ExperimentOutside/random/GPS/GPS_CAD"
cast(File_Path, "GPS")
