import numpy as np
from statistics import mean
import pandas as pd
import os
import glob
import shutil


def interpol(data):
    new1 = pd.DataFrame()
    print(len(data.x))
    print(data.x[0])   # [x1 12345678910 x2][x2     x3]
    for i in range(0, len(data.x), 1):
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


def cast(data_dir, typ, sub_folders):
    directory = typ+"_Interpolated_test"
    for i in range(0, len(sub_folders), 1):
        path = os.path.join(data_dir, sub_folders[i])
        path2 = os.path.join(path, directory)
        os.chdir(path)
    # overwrite if already exists
        if os.path.exists(path2):
            print("Path already exists' Override!")
            shutil.rmtree(path2)
        os.mkdir(path2)
        csv_files = glob.glob(os.path.join(path, "*.csv"))
        print(csv_files)
        for i in csv_files:
            a = interpol(pd.read_csv(i))
            i = i[:i.rfind('.csv')]
            a.to_csv(i+"_Interpolated.csv")
            shutil.move(i+"_Interpolated.csv", path2)

    print("\n End of trial, No Errors!")


data_dir = "/Users/anasosman/Downloads/Terrece_Experiment/GPS_Terrace"
sub_folders = os.listdir(data_dir)
sub_folders.remove(".DS_Store")
print(sub_folders)
cast(data_dir, "GPS", sub_folders)
