# This Repo contains the Scripts for processing the UWB raw data

## Translation of UWB raw data onto the CAD coordinates 
The first step involves the translation of UWB raw data onto the CAD coordinates of the Garage and The Terrace depending on which experiment was performed.

#### In the case of UWB:

* To run the script, you need the directory name that contains all the UWB data. 
Example: "Users/username/Downloads/Experiment_in_the_Terrace_UWB"

* It requires the offset.r script that performs the offset calculation process and the R environment directory path.

The output includes [(UWB_Offset: the UWB coordinates after applying the **GPS** to **UWB** offset), (UWB_CAD: the converted coordinates), (UWB_AutoCAD: AutoCAD File used for visualization)] Note: The Cad conversion is applied after applying the Device offset first.

#### In the case of GPS/Cohda:

To run the file it requires the directory name that contains all the UWB data for Example: "Users/username/Downloads/Experimentin_the_Terrace_GPS", Usually for GPS-only one file is required for Cohda each experiment has its own separate file.

## Time alignment

Both the GPS/ Cohda and the UWB samples are time synchronized with NTP. The output of both devices runs at 10 Hz, so the two share almost similar timestamps.

The script outputs data that match the UWB_data comparing them both using timestamps.

To run this script it requires the directories that include the UWB data and the GPS/Cohda, the output of this script is moved by default to the UWB directory.

## Interpolation

This script is used to up-sample the given data. It adds 10 points between every two pairs of points to perform distance error analysis.

To run this script it requies the directory that include the UWB_Cad data or the GPS_Cad/Cohda_Cad data.

## The index offset

Includes the performance of index offset analysis in-order to assis if there is a sampling gap between the GPS/Cohda and UWB while the car is moving at diffrent speeds.

To run this it requires the UWB directory path andpath of the directory of the GPS.

## Alignment_Without_Skipping.

A script used to analyze the raw UWB data fix the sampling issues with the timestamps and perform a proper time alignment with Cohda/GPS.

In case of missing data the script accounts for it in the form of averaging the two closest values.
