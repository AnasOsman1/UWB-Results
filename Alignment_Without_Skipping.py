import pandas as pd
import os
import glob
import numpy as np
import math
import time

# Script for Fixing the UWb and analyzing the missing data
counter = 0
data_dir = "/Users/anasosman/Downloads/Terrece_Experiment/Experiment_Terrace"
sub_folders = os.listdir(data_dir)


def align(s):
    x = pd.DataFrame()
    for i in range(1, len(s), 1):
        if s.time_stamps[i] - s.time_stamps[i].astype(int) >= 0.85:
            # val = pd.DataFrame({"time": math.floor(s.time_stamps[i])})
            # val = list(math.floor(s.time_stamps[i]))
            # val.append(val)
            # print(s.time_stamps.index[i], s.time_stamps[i], math.ceil(
            # s.time_stamps[i]))
            m = math.ceil(s.time_stamps[i])
            result = pd.DataFrame(
                {"time_stamps": m}, index=[i])
            x = pd.concat([x, result])
            # print(data)
            # continue
        else:
            m = math.floor(s.time_stamps[i])
            result = pd.DataFrame(
                {"time_stamps": m}, index=[i])
            # n = pd.concat([n, result])
            x = pd.concat([x, result])
    return x


for i in range(1, len(sub_folders), 1):
    path = os.path.join(data_dir, sub_folders[i])
    os.chdir(path)
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    for i in csv_files:
        print(i)
        UWB = pd.read_csv(i)
# GPS = pd.read_csv("/Users/anasosman/Downloads/2022.10.14_2_terrace_afternoon/novatel_cad.csv")
        a = pd.DataFrame()
        b = pd.DataFrame()
        a['time_stamps'] = (UWB.rosbagTimestamp/10**8)
        s = a.round(2)
        z = align(s)
        # print(z)
    # print(s.time_stamps[2])
        for k in range(1, len(z.time_stamps)-1, 1):
            #       #    #  for j in range(1, len(b)-1, 1):
            #       #    #      if a.time_stamps[i] == b.time_stamps[j]:
            #       #    #          print(b.time_stamps.index[j])
            seq = z.time_stamps[k+1] - z.time_stamps[k]
            if (seq == 2):
                print(z.time_stamps.index[k], z.time_stamps.index[k+1],
                      z.time_stamps[k], z.time_stamps[k+1], seq)
            elif (seq > 2):
                print(z.time_stamps.index[k], z.time_stamps.index[k+1],
                      z.time_stamps[k], z.time_stamps[k+1], seq)
            else:
                continue
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
#
