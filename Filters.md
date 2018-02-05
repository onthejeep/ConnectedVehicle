# Connected Vehicle, THEA, Tampa
## Study Area
The study area is pre-defined by local transit agency and academic research group. The area is in an ArcGIS shapefile (*.shp) format, and can be found under the folder "data\StudyArea.shp".

## Message Split
Raw data receieved from THEA is organized in CSV format. Four columns are mainly included in raw data. Table 1 lists the details of the four columns. Table 2 shows examples of raw data.

Table 1. Columns in raw data

| Column Name | Description |
| ----------- | ----------- |
| timestamp | Unix timestamp in millisecond |
| kind | Always “in” for now |
| psid | Message type ID. 32 for BSM; 32770 for SPAT |
| payload | XML encoded J2735 message |

Table 2. Examples of raw data

| timestamp | kind | psid | payload |
| 1512500403618 | in | 32 | <MessageFrame><messageId>20</messageId><value><BasicSafetyMessage><coreData><msgCnt>93</msgCnt><id>6G956739</id><secMark>3699</secMark><lat>279527625</lat><long>-824491237</long><elev>-172</elev><accuracy><semiMajor>6</semiMajor><semiMinor>5</semiMinor><orientation>20780</orientation></accuracy><transmission><unavailable></unavailable></transmission><speed>0</speed><heading>14608</heading><angle>127</angle><accelSet><long>5</long><lat>10</lat><vert>0</vert><yaw>1</yaw></accelSet><brakes><wheelBrakes>10000</wheelBrakes><traction><unavailable></unavailable></traction><abs><unavailable></unavailable></abs><scs><unavailable></unavailable></scs><brakeBoost><unavailable></unavailable></brakeBoost><auxBrakes><unavailable></unavailable></auxBrakes></brakes><size><width>267</width><length>508</length></size></coreData><partII><SEQUENCE><partII-Id>0</partII-Id><partII-Value><VehicleSafetyExtensions><pathHistory><crumbData><PathHistoryPoint><latOffset>-6155</latOffset><lonOffset>-260</lonOffset><elevationOffset>79</elevationOffset><timeOffset>13554</timeOffset></PathHistoryPoint><PathHistoryPoint><latOffset>-10995</latOffset><lonOffset>-998</lonOffset><elevationOffset>82</elevationOffset><timeOffset>13865</timeOffset></PathHistoryPoint><PathHistoryPoint><latOffset>-14674</latOffset><lonOffset>-2263</lonOffset><elevationOffset>78</elevationOffset><timeOffset>14065</timeOffset></PathHistoryPoint><PathHistoryPoint><latOffset>-18198</latOffset><lonOffset>-4349</lonOffset><elevationOffset>64</elevationOffset><timeOffset>14255</timeOffset></PathHistoryPoint><PathHistoryPoint><latOffset>-21215</latOffset><lonOffset>-7012</lonOffset><elevationOffset>47</elevationOffset><timeOffset>14434</timeOffset></PathHistoryPoint></crumbData></pathHistory><pathPrediction><radiusOfCurve>32767</radiusOfCurve><confidence>200</confidence></pathPrediction></VehicleSafetyExtensions></partII-Value></SEQUENCE></partII></BasicSafetyMessage></value></MessageFrame>|
| 1512500406617 | in | 32 | <MessageFrame><messageId>20</messageId><value><BasicSafetyMessage><coreData><msgCnt>123</msgCnt><id>6G956739</id><secMark>6700</secMark><lat>279527625</lat><long>-824491235</long><elev>-173</elev><accuracy><semiMajor>6</semiMajor><semiMinor>5</semiMinor><orientation>20352</orientation></accuracy><transmission><unavailable></unavailable></transmission><speed>0</speed><heading>14608</heading><angle>127</angle><accelSet><long>2</long><lat>3</lat><vert>0</vert><yaw>1</yaw></accelSet><brakes><wheelBrakes>10000</wheelBrakes><traction><unavailable></unavailable></traction><abs><unavailable></unavailable></abs><scs><unavailable></unavailable></scs><brakeBoost><unavailable></unavailable></brakeBoost><auxBrakes><unavailable></unavailable></auxBrakes></brakes><size><width>267</width><length>508</length></size></coreData><partII><SEQUENCE><partII-Id>0</partII-Id><partII-Value><VehicleSafetyExtensions><pathHistory><crumbData><PathHistoryPoint><latOffset>-6155</latOffset><lonOffset>-258</lonOffset><elevationOffset>78</elevationOffset><timeOffset>13855</timeOffset></PathHistoryPoint><PathHistoryPoint><latOffset>-10995</latOffset><lonOffset>-996</lonOffset><elevationOffset>81</elevationOffset><timeOffset>14165</timeOffset></PathHistoryPoint><PathHistoryPoint><latOffset>-14674</latOffset><lonOffset>-2261</lonOffset><elevationOffset>77</elevationOffset><timeOffset>14365</timeOffset></PathHistoryPoint><PathHistoryPoint><latOffset>-18198</latOffset><lonOffset>-4347</lonOffset><elevationOffset>63</elevationOffset><timeOffset>14555</timeOffset></PathHistoryPoint><PathHistoryPoint><latOffset>-21215</latOffset><lonOffset>-7010</lonOffset><elevationOffset>46</elevationOffset><timeOffset>14735</timeOffset></PathHistoryPoint></crumbData></pathHistory><pathPrediction><radiusOfCurve>32767</radiusOfCurve><confidence>200</confidence></pathPrediction></VehicleSafetyExtensions></partII-Value></SEQUENCE></partII></BasicSafetyMessage></value></MessageFrame> |


## Basic Safety Message (BSM) Filter
BSM filter is implemented in Python. The filter currently includes two parts:
1. Geofence
Only vehicle positions located in the pre-defined study area are provided; positions out of the study area are filtered out
2. Vehicle ID scramble
Several encryption methods are implemented to encrpy vehicle ID, and then write encrpied IDs back to original message.
The filtered files follow the orginal files' name, but saved under the folder "filtered".

## Signal Phase and Timing (SPAT) Filter
SPAT filter is implemented in Python. Under development.


