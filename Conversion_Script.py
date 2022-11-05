#!/usr/bin/env python3.
# Performing Trilateration on a Give 3 Points
from operator import index
import numpy
import math
import pandas as pd
import os
import glob
import shutil

# Globals
# Terrace Refrance Points
Lat1 = 46.0677393
Lon1 = 11.15091824
Lat2 = 46.06762059
Lon2 = 11.15071904
Lat3 = 46.06799005
Lon3 = 11.15072119

# Refracance Points for Garage
'''
Lat1 = 46.06755685
Lon1 = 11.15094179
Lat2 = 46.06744994
Lon2 = 11.1516506
Lat3 = 46.06803331
Lon3 = 11.15160491
'''

# Hervestine Distance between Lat1/ Lon1 to Lat2/Lon2

def dis_calc_herv(Lat1, Lon1, Lat2=[], Lon2=[]):
    earthR = 6356.137  # in Km

    latA = numpy.radians(Lat1)
    lonA = numpy.radians(Lon1)
    latB = numpy.radians(Lat2)
    lonB = numpy.radians(Lon2)

    dlon = lonB - lonA
    dlat = latB - latA

    a = pow(numpy.sin(dlat / 2), 2) + numpy.cos(latA) * \
        numpy.cos(latB) * pow(numpy.sin(dlon / 2), 2)
    c = 2 * numpy.arctan2(numpy.sqrt(a), numpy.sqrt(1 - a))

    distance = earthR * c

    return distance*pow(10, 3)  # Conv to meters

# Distance between Two Points in XY


def xy_distance(x1, y1, x=[], y=[]):

    # Standard Distance Equation
    radius = numpy.sqrt(pow(x1-x, 2)+pow(y1-y, 2))

    return radius

# Triliterataion XY in meters


def Tri_conv(r1, r2, r3, Time):

    # UWB Refracance CAD Points
    x1 = 100.23
    y1 = 50.84
    x2 = 113.47
    y2 = 35.59
    x3 = 72.48
    y3 = 35.51

    '''
    x1 = 120.3
    x2 = 132.7
    x3 = 67.24
    y1 = 51.11
    y2 = 108.15
    y3 = 103.71
    '''

    A = 2*x2 - 2*x1
    B = 2*y2 - 2*y1
    C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2*x3 - 2*x2
    E = 2*y3 - 2*y2
    F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)
    #Time = Time/pow(10, 8)
    new = {
        'time_stamps': Time,
        'x': round(x, 4),
        'y': round(y, 4),
        'z': 0  # for cad conversion
    }
    l = pd.DataFrame(new)
    # for AutoCAD Script Covnversion
    symp = ','
    l['AutoCAD Format'] = l['x'].astype(
        str)+","+l['y'].astype(str)+","+l['z'].astype(str)
    l.index = numpy.arange(1, len(l.x)+1)
    return(l)

# Conversion to CAD XY
def Conversion(File_Path, type):

    data_dir = File_Path
    sub_folders = os.listdir(data_dir)
    for i in range(1, len(sub_folders), 1):
        path = os.path.join(data_dir, sub_folders[i])
        os.chdir(path)
        csv_files = glob.glob(os.path.join(path, "*.csv"))
    # directory change
        directory = type+"_CAD"
        directory2 = "UWB_AutoCAD_Script"
        directory3 = "UWB_Offset"
        path2 = os.path.join(path, directory)
        path3 = os.path.join(path2, directory2)
        path4 = os.path.join(path, directory3)

    # overwrite if already exists
        if os.path.exists(path2):
            shutil.rmtree(path2)
        os.mkdir(path2)
        if os.path.exists(path3):
            shutil.rmtree(path3)
        os.mkdir(path3)
        if os.path.exists(path4):
            shutil.rmtree(path4)
        os.mkdir(path4)

    # loop over the list of csv files
        for i in csv_files:
            n = i[:i.rfind('.csv')]
            # read the csv file
            if(type == "UWB"):
                # Imposing the Device Offset 0.09cm
                os.system(
                    "/Library/Frameworks/R.framework/Versions/4.0/Resources/Rscript"+" "+"/Users/anasosman/Downloads/offset.r"+" " + i+" " + n+"_offset.csv")
                data = pd.read_csv(n+"_offset.csv")
                shutil.move(n+"_offset.csv", path4)
                UWB = pd.DataFrame(Tri_conv(xy_distance(0.24, 17.82, data["x"], data["y"]),
                                            xy_distance(-15.01, 4.58,
                                                        data["x"], data["y"]),
                                            xy_distance(-15.09, 45.57, data["x"], data["y"]), data["rosbagTimestamp"]))
                i = i[:i.rfind('.csv')]
                UWB.to_csv(i+"_cad.csv")
                shutil.move(i+"_cad.csv", path2)
                with open(i+"_cad.scr", "w") as f_out:  # Autocad script files creation
                    content = "\n".join(UWB['AutoCAD Format'])
                    new_line = "_MULTIPLE _POINT\n"
                    f_out.write(new_line + content)
                    shutil.move(i+"_cad.scr", path3)

            elif(type == "GPS"):
                col_list = ['lat', 'lon', 'time_us']
                data = pd.read_csv(i, usecols=col_list)
                GPS = pd.DataFrame(Tri_conv(dis_calc_herv(Lat1, Lon1, data["lat"], data["lon"]),
                                            dis_calc_herv(
                    Lat2, Lon2, data["lat"], data["lon"]),
                    dis_calc_herv(Lat3, Lon3, data["lat"], data["lon"]), data["time_us"]))
                i = i[:i.rfind('.csv')]
                GPS.to_csv(i+"_cad.csv")
                shutil.move(i+"_cad.csv", path2)


# Function Invoked when Given Path and type of Conversion
Conversion(
    "/Users/anasosman/Downloads/ExperimentOutside", "UWB")
