# Connected Vehicle, THEA, Tampa
## Study Area
The study area is pre-defined by local transit agency and academic research group. The area is in an ArcGIS shapefile (*.shp) format, and can be found under the folder "data\StudyArea.shp".

## Message Split
Raw data receieved from THEA is organized in CSV format. Four columns are mainly included in raw data. Table 1 lists the details of the four columns. Table 2 shows examples of raw data.

Table 1. Columns in raw data

| Column Name | Description |
| ----------- | ----------- |
| timestamp | UNIX timestamp in millisecond |
| kind | Always “in” for now |
| psid | Message type ID. 32 for BSM; 32770 for SPAT |
| payload | XML encoded J2735 message |

Table 2. Examples of raw data

| timestamp | kind | psid | payload |
| ----------- | ---- | ---- | ----------------------- |
| 1512500403618 | in | 32 | XML encoded J2735 message |
| 1512500406617 | in | 32 | XML encoded J2735 message |

## Message Filter
### Basic Safety Message (BSM) Filter
BSM filter is implemented in Python. The filter currently includes two parts:
1. Geofence
Only vehicle positions located in the pre-defined study area are provided; positions out of the study area are filtered out
2. Vehicle ID scramble
Several encryption methods are implemented to encrpy vehicle ID, and then write encrpied IDs back to original message.
The filtered files follow the orginal files' name, but saved under the folder "filtered".

### Signal Phase and Timing (SPAT) Filter
SPAT filter is implemented in Python. Under development.

## Meta Data
Meta data is developed to provide additional information about other data.

### Basic Safety Message (BSM) Meta Data
The BSM meta data includes:

| Field Name | Definition |
| ---- | ----------- |
| schemaVersion | Version of the metadata schema |
|recordGeneratedBy|Source of the record, whether OBU, RSU, MMITSS|
|recordGeneratedAt|Closest time to which the record was created, either signed or received by the generatedBy source in UNIX format|
|logFileName|Name of original files that receieved by CUTR CV Performance Evaluation group|
|logFileSize|File size of original files that receieved by CUTR CV Performance Evaluation group|
|payloadType|Type of payload included with the message|
|recordType|Type of message|
|numRecord|Number of records in original files|
|serialId|Unique record identifier for message |
|serialId/bundledId|Bundle identifier|
|serialId/recordId|Sequence number of record in original files|
|bsmSource|Source of the BSM. Host vehicle = EV, Remote vehicle = RV|
|securityResultCode|Status of IEEE 1609.2 security validation|

An example of meta and message is shown below. The example is presented in JSON format.

```json
{
	"metadata": {
		"schemaVersion": 1,
		"recordGeneratedBy": "OBU",
		"recordGeneratedAt": "2017-12-05 14:18:28.114 [ET]",
		"logFileName": "2017_12_5_13_rsu40.csv",
		"logFileSize": "1633670 byte",
		"payloadType": "BsmPayload",
		"recordType": "bsmTx",
		"numRecord": 637,
		"serialId": {
			"bundledId": 0,
			"recordId": 5
		},
		"bsmSource": "CV",
		"securityResultCode": "unknown"
	},
	"payload": {
		"dataType": "j2735.J2735Bsm",
		"data": {
			"coreData": {
				"msgCnt": "60",
				"id": "FE95E8G3",
				"secMark": "28150",
				"lat": "279495645",
				"long": "-824576935",
				"elev": "-152",
				"accuracy": {
					"semiMajor": "13",
					"semiMinor": "9",
					"orientation": "26655"
				},
				"transmission": {
					"unavailable": null
				},
				"speed": "382",
				"heading": "20205",
				"angle": "127",
				"accelSet": {
					"long": "-162",
					"lat": "55",
					"vert": "0",
					"yaw": "310"
				},
				"brakes": {
					"wheelBrakes": "10000",
					"traction": {
						"unavailable": null
					},
					"abs": {
						"unavailable": null
					},
					"scs": {
						"unavailable": null
					},
					"brakeBoost": {
						"unavailable": null
					},
					"auxBrakes": {
						"unavailable": null
					}
				},
				"size": {
					"width": "201",
					"length": "435"
				}
			},
			"partII": {
				"SEQUENCE": {
					"partII-Id": "0",
					"partII-Value": {
						"VehicleSafetyExtensions": {
							"pathHistory": {
								"crumbData": {
									"PathHistoryPoint": [{
											"latOffset": "-43",
											"lonOffset": "-148",
											"elevationOffset": "0",
											"timeOffset": "20"
										}, {
											"latOffset": "-8975",
											"lonOffset": "-26545",
											"elevationOffset": "11",
											"timeOffset": "2460"
										}
									]
								}
							},
							"pathPrediction": {
								"radiusOfCurve": "1527",
								"confidence": "200"
							}
						}
					}
				}
			}
		}
	}
}

```

### Signal Phase and Timing (SPAT) Meta Data
