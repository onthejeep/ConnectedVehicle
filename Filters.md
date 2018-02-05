# Connected Vehicle, THEA, Tampa
## Study Area
The study area is pre-defined by local transit agency and academic research group. The area is in an ArcGIS shapefile (*.shp) format, and can be found under the folder "data\StudyArea.shp".

## Message Split
Raw data receieved from THEA is organized in CSV format. Four columns are mainly included in raw data. Table 1 lists the details of the four columns.

Table 1. Columns in Raw Data
| Column Name | Description |
| ----------- | ----------- |
| timestamp | Unix timestamp in millisecond |
| kind | always “in” for now |
| psid | message type ID. 32 for BSM; 32770 for SPAT |
| payload | XML encoded J2735 message |



## Basic Safety Message (BSM) Filter
BSM filter is implemented in Python. The filter currently includes two parts:
1. Geofence
Only vehicle positions located in the pre-defined study area are provided; positions out of the study area are filtered out
2. Vehicle ID scramble
Several encryption methods are implemented to encrpy vehicle ID, and then write encrpied IDs back to original message.
The filtered files follow the orginal files' name, but saved under the folder "filtered".

## Signal Phase and Timing (SPAT) Filter
SPAT filter is implemented in Python. The filter currently includes single parts:
1. Geofence
Only vehicle positions located in the pre-defined study area are provided; positions out of the study area are filtered out
Vehicle ID scramble: Several encryption methods are implemented to encrpy vehicle ID, and then write encrpied IDs back to original message.
The filtered files follow the orginal files' name, but saved under the folder "filtered".


