import pandas as pd
import os
import glob
import numpy as np
import math
import time
import shutil

# Script for Fixing the UWb and analyzing the missing data
# data_dir = "/Users/anasosman/Downloads/2022.10.14_2_terrace_afternoon"  # Garage
data_dir = "/Users/anasosman/Downloads/Experiment_Garage"
sub_folders = os.listdir(data_dir)
directory = "GPS_Aligned"
directory3 = "UWB_Modified"
path2 = os.path.join(data_dir, directory3)

# overwrite if already exists
if os.path.exists(path2):
    shutil.rmtree(path2)
os.mkdir(path2)

a = pd.DataFrame()
b = pd.DataFrame()

# Fixing the Data


def point(z, k, seq):
    df = pd.DataFrame()
    df2 = pd.DataFrame()
    new_time = np.linspace(z.time_stamps[k], z.time_stamps[k+1], seq-1)
    # finding the average distance between 2 points in x
    px = np.linspace(z.x[k+1], z.x[k], seq-1)
    # finding the average distance between 2 points in y
    py = np.linspace(z.y[k+1], z.y[k], seq-1)
    # arr = np.ndarray[{"time_stamps": new_time}, {"x": px}, {"y", py}]
    # col = ["new_time", "x", "y"]
    # print(new_time, seq)
    # print(new_time)
    # finding the average distance between 2 points in
    # df = pd.DataFrame(arr, columns=cols)
    df = pd.DataFrame({"time_stamps": new_time, "x": px, "y": py})
    df2 = pd.concat([df2, df])
    # Create copy of DataFrame
    data_new = z.copy()
# Append list at the bottom
    dff = pd.concat([z.x.loc[k],  pd.DataFrame(
        {"time_stamps": new_time, "x": px, "y": py}), z.x.loc[k+1]], ignore_index=False)
    # data_new.loc[z[k]] = df
    # df2 = data_new.sort_index().reset_index(drop=False)
    # df2 = pd.concat([z.iloc[k+1:], df, z.iloc[k+1:]]).reset_index(drop=False)
    # df2 = df.sort_index().reset_index(drop=False)
    return dff


def align(s):
    x = pd.DataFrame()
    for i in range(0, len(s), 1):
        if (s.time_stamps[i] - s.time_stamps[i].astype(int)) >= 0.9:
            # val = pd.DataFrame({"time": math.floor(s.time_stamps[i])})
            # val = list(math.floor(s.time_stamps[i]))
            # val.append(val)
            # s.time_stamps[i]))
            # print(s.time_stamps.index[i], s.time_stamps[i])  # Check Before
            m = math.ceil(s.time_stamps[i])
            result = pd.DataFrame(
                {"time_stamps": m, "x": s.x[i], "y": s.y[i]}, index=[i])
            x = pd.concat([x, result])
            # print(data)
            # continue
        else:
            m = math.floor(s.time_stamps[i])
            result = pd.DataFrame(
                {"time_stamps": m, "x": s.x[i], "y": s.y[i]}, index=[i])
            # n = pd.concat([n, result])
            x = pd.concat([x, result])
    return x

# GPS/COHDA time alignment with UWB


def time_alignment(b, z):
    y = pd.DataFrame()
    for j in range(1, len(b), 1):
        for k in range(0, len(z.time_stamps), 1):
            if z.time_stamps[k] == b.time_stamps[j]:
                x = pd.DataFrame(
                    {"time_stamps": b.time_stamps[j], "x": b.x[j], "y": b.y[j]}, [k])
                y = pd.concat([y, x])
    return y


#### WHERE I MODIFIED THE CODE!!! ####

# Function that outputs a dataframe containing the missing points
def insertMissingPoints(z, k, diff):
    new_time = np.linspace(
        z.time_stamps[k], z.time_stamps[k+1], diff+1, endpoint=True)
    # finding the average distance between 2 points in x
    px = np.linspace(z.x[k], z.x[k+1], diff+1, endpoint=True)
    py = np.linspace(z.y[k], z.y[k+1], diff+1, endpoint=True)
    for i in range(len(px)):
        px[i] = np.round(px[i], 2)
    # finding the average distance between 2 points in y
    for i in range(len(py)):
        py[i] = np.round(py[i], 2)
    np.round(py, 2)
    # print(py)
    data = {"time_stamps": new_time[:diff],
            "x": px[:diff], "y": py[:diff]}
    rows = pd.DataFrame(
        data, columns=["time_stamps", "x", "y"])
    return rows


for i in range(1, len(sub_folders), 1):
    path = os.path.join(data_dir, sub_folders[i])
    os.chdir(path)
    path2 = os.path.join(path, directory3)
    path3 = os.path.join(path, directory)
    if os.path.exists(path2):
        shutil.rmtree(path2)
    os.mkdir(path2)
    if os.path.exists(path3):
        shutil.rmtree(path3)
    os.mkdir(path3)
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    for i in csv_files:
        print(i)
        df = pd.DataFrame()
        cols = ["rosbagTimestamp", "x", "y"]
        UWB = pd.read_csv(i, usecols=cols)
        cols2 = ["time_stamps", "x", "y"]
        GPS = pd.read_csv(
            "/Users/anasosman/Downloads/2022.10.14_2_terrace_afternoon/GPS/novatel_cad.csv")
        a = UWB.reset_index()
        b = GPS
        a['time_stamps'] = (UWB.rosbagTimestamp/10**8)
        b['time_stamps'] = (GPS.time_stamps/100).astype(int)
        s = a.round(2)
        # z = align(b) # for GPS missing values
        z = align(s)  # for UWB missing values
        # print(z)
        # print(s.time_stamps[2])
        # to check before we can add s instead of z

        # this is the new dataframe with no missing point ideally.
        new_uwb = pd.DataFrame(columns=["time_stamps", "x", "y"])
        for k in range(0, len(z.index)-1, 1):
            # print(k)
            # difference between consecutive timestamps
            diff = z.time_stamps.loc[k+1] - z.time_stamps.loc[k]
            # Case in which there is no difference. Just concatenate the old dataframe line to the new one
            if diff <= 1:
                # print(diff)
                # new_uwb.loc[-1].append(z.loc[k])
                new_uwb.loc[len(new_uwb.index)] = z.loc[k]
            # The difference is more than 1 --> create the new dataframe with the missing points and
            # concatenate it to the bottom of the new dataframe
            else:
                # print(k)
                print("Number of Missing points", diff-1)
                rows = insertMissingPoints(z, k, diff)
                # print(diff)
                new_uwb = pd.concat([new_uwb, rows])
                new_uwb.reset_index(drop=True, inplace=True)
                # print(len(new_uwb.index)-(k+1))
        #
        i[:i.rfind('.csv')]
        new_uwb.to_csv(i+"_modification.csv")
        shutil.move(i+"_modification.csv", path2)
        print("Lenght Diffrances: ", len(new_uwb.x) - len(UWB.x))
        l = time_alignment(b, new_uwb)
        i[:i.rfind('.csv')]
        l.to_csv(i+"_gps.csv")
        shutil.move(i+"_gps.csv", path3)

    # z.to_csv("old_uwb.csv")


##################################

    # for k in range(1, len(z.time_stamps)-1, 1):
    #     # for j in range(1, len(b)-1, 1):
    #     # if z.time_stamps[k] == b.time_stamps[j]:
    #     # print(b.time_stamps[1], z.time_stamps[1])
    #     seq = (z.time_stamps[k+1] - z.time_stamps[k])
    #     if (seq <= 1):  # one missing point
    #         # print(z.time_stamps.index[k], z.time_stamps.index[k+1],z.time_stamps[k], z.time_stamps[k+1], seq)
    #         g = z
    #         df = pd.concat([df, g])
    #     elif (seq == 2):
    #         # print(z.time_stamps.index[k], z.time_stamps.index[k+1],z.time_stamps[k], z.time_stamps[k+1], seq)
    #         g = point(z, k, seq)
    #         # print(point(z, k, seq))
    #         df = pd.concat([df, g])
    #     elif (seq > 2):  # 2 < missing points
    #         # print(z.time_stamps.index[k], z.time_stamps.index[k+1], z.time_stamps[k], z.time_stamps[k+1], seq)
    #         g = point(z, k, seq)
    #         df = pd.concat([df, g])
    # print(len(z.x)-len(g.x))
    # g.to_csv(j+"_modification.csv")


# print(n)
# time.sleep(5)
# n.to_csv("/Users/anasosman/Downloads/01.csv")
# print(result.get('time_stamps')[1])
# print(data)
# val = pd.DataFrame({"time": math.ceil(s.time_stamps[i])})
# val.append(val)
# print(math.ceil(s.time_stamps[i]))
# n = pd.concat([n, val])
# print(val)
# b['time_stamps'] = (GPS.time_sstamps/100).astype(int)

# print(k)
# for i in range(1, len(k.time_stamps)-1, 1):
#    #       #    #  for j in range(1, len(b)-1, 1):
#    #       #    #      if a.time_stamps[i] == b.time_stamps[j]:
#    #       #    #          print(b.time_stamps.index[j])
#    if k.time_stamps[i+1] - k.time_stamps[i] >= 2:
#        seq = k.time_stamps[i+1] - k.time_stamps[i]
#        #           # print(seq)
#    else:
#        continue
#        #   # else:       #
#    # print(  # counter)
#
#    # def align(UWB, GPS):
#    for j in range(1, len(UWB.rosbagTimestamp), 1):
#        for i in range(1, len(GPS.time_us), 1):
#            if UWB.rosbagTimestamp[j] <= GPS.time_us[i]:
#                print("good")
#            else:
#                continue

# align(UWB, GPS)

# data = pd.DataFrame()

# class ProcessData():

#    def __init__(self, frame):
#        self.data = frame

#   def time(self):
#      return (self.data['time_stamps'])
#
# def __contains__(self, value):
# if value in self.val:
#        return True
#      else:
# return False
