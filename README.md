# This Repo contains the Scripts for processing the UWB raw data

## Translation of UWB raw data onto the CAD coordinates 
The first step involves the Translation of UWB raw data onto the CAD coorinates 
of the Garage and The Terrace depending on which experiment was performed. 

#### In case of UWB:

* To run the file it requires the directory name that contains all the UWB data for 
Example: "Users/username/Downloads/Experiment_in_the_Terrace_UWB"

* It requires the offset.r script that performs the offset calculation process and the R envirnoment directory path.

The output includes [(UWB_Offset: the UWB coordiantes after applying the GPS to UWB offset),(UWB_CAD: the converted coordinates), 
(UWB_AutoCAD:AutoCAD File used for visualization)] Note: The Cad conversion is applied after applying the Device offset first.

#### In case of GPS/Cohda:

To run the file it requires the directory name that contains all the UWB data for 
Example: "Users/username/Downloads/Experimentin_the_Terrace_GPS", Usually for the GPS only one file is required for Cohda each experiment
has its own seperate file.


## Time Alignment

Since the two samples extracted from the GPS/ Cohda and the UWB are time synchronzied with NTP server. 
The output of both devices is in 10 Hz, hence the two share almost similar timestamps.

The script outputs data that match the UWB_data comparing them both using timestamps.

To run this script it requies the directories that include the UWB data and the GPS/Cohda, the output of this script is 
moved by defult to the UWB directory.

## Interpolation

This script is used to up-sample given data. It adds 10 points between each two paris of points to perform the distance error analysis.

To run this script it requies the directory that include the UWB_Cad data or the GPS_Cad/Cohda_Cad data.

## The index offset

Includes the performance of index offset analysis in-order to assis if there is a sampling gap between the GPS/Cohda and UWB
while the car is moving at diffrent speeds.

To run this it requires path of the directory of UWB and the path of the directoy of the GPS



