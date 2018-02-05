import datetime;
import os;
import pytz;
import time;
import pandas as pan;
import xmltodict;
import Connect2DB;

class ImportRSU:

    def __init__(self):
        self.__Connection__ = None;

    def SetupConnction(self):
        self.__Connection__  = Connect2DB.Connect2MSSQL.GetInisitance_ODBC();

    def PathHistorySinglePoint(self, point):
        PointInfo = '{},{},{},{};'.format(point['latOffset'], point['lonOffset'], point['elevationOffset'], point['timeOffset']);
        return(PointInfo);

    def PathHistoryPoints(self, points):
        Points = '';
        NumPoints = len(points);
        for i in range(NumPoints):
            Points += self.PathHistorySinglePoint(points[i]);

        return(Points);

    def ConvertLatLong(self, strNumber):
        pass;
        #Length = 0;
        #if strNumber[0] == '-':
        #    Length = len(strNumber) - 1

    def ImportRSU(self, fileName, rsu_station):

        DataTable = pan.read_csv(fileName, skipinitialspace = True, index_col = None, header = None);
        InsertCursor = self.__Connection__.cursor();

        for i in range(DataTable.shape[0]):
            Label = int(DataTable[2][i]);
            if Label != 32:
                continue;

            print(i);
            UnixTime = float(DataTable[0][i]) / 1000;
            Timestamp = datetime.datetime.fromtimestamp(UnixTime).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3];

            BSM = DataTable[3][i];
            BSM_Xml = xmltodict.parse(BSM);

            MessageID = BSM_Xml['MessageFrame']['messageId'];
            Core_MsgCnt = BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['msgCnt'];
            Core_ID = BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['id'];
            Core_SecMark = BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['secMark'];
            Core_Lat = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['lat']) / 1e7;
            Core_Long = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['long']) / 1e7;
            Core_Elev = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['elev']) * 0.1; # meter
            Acc_SemiMajor = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['accuracy']['semiMajor']) * 0.05; # meter
            Acc_SemiMinor = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['accuracy']['semiMinor']) * 0.05; # meter
            Acc_Orientation = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['accuracy']['orientation']) * 360 / 65535;
            Transmission = BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['transmission'];
            Speed = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['speed']) * 0.02; # m/s
            Heading = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['heading']) * 0.0125; # degree 
            Angle = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['angle']) * 1.5; # degree
            AccelSet_Long = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['accelSet']['long']) * 0.01; # m/s^2
            AccelSet_Lat = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['accelSet']['lat']) * 0.01; # m/s^2
            AccelSet_Vert = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['accelSet']['vert']) * 0.1962; # m/s^2
            AccelSet_Yaw = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['accelSet']['yaw']) * 0.01; # degree/second
            Brakes_WheelBrakes = BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['brakes']['wheelBrakes'];
            Brakes_Traction = BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['brakes']['traction'];
            Brakes_Abs = BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['brakes']['abs'];
            Brakes_Scs = BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['brakes']['scs'];
            Brakes_BrakeBoost = BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['brakes']['brakeBoost'];
            Brakes_AuxBrakes = BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['brakes']['auxBrakes'];
            Size_Width = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['size']['width']) * 0.01;
            Size_Length = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['size']['length']) * 0.01;

            Sequence_ID = BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['partII']['SEQUENCE']['partII-Id'];
            PathHistory_Point = BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['partII']['SEQUENCE']['partII-Value']['VehicleSafetyExtensions']['pathHistory']['crumbData']['PathHistoryPoint'];
            PathPrediction_Radius = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['partII']['SEQUENCE']['partII-Value']['VehicleSafetyExtensions']['pathPrediction']['radiusOfCurve']) * 0.1; # meter
            PathPrediction_Confidence = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['partII']['SEQUENCE']['partII-Value']['VehicleSafetyExtensions']['pathPrediction']['confidence']) * 0.5; # percent

            PointsInfo = self.PathHistoryPoints(PathHistory_Point);

            InsertCommand = """insert into [ConnectedVehicle].[dbo].[RSU_Temp] ([RSU.Station], [Timestamp], [PSID], [MessageID],[Core.MsgCnt],[Core.ID],[Core.SecMark],\
            [Core.Lat],[Core.Long] \
,[Core.Elev],[Acc.SemiMajor],[Acc.SemiMinor],[Acc.Orientation],[Speed],[Heading],[Angle],[AccelSet.Long],[AccelSet.Lat],[AccelSet.Vert] \
,[AccelSet.Yaw],[Brakes.WheelBrakes],[Size.Width],[Size.Length],[Sequence.ID],[PathHistory.Point],[PathPrediction.Radius] \
,[PathPrediction.Confidence]) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""";
            
            InsertCursor.execute(InsertCommand, (rsu_station, Timestamp, Label, MessageID, Core_MsgCnt, Core_ID, Core_SecMark, 
                                                 Core_Lat, Core_Long, 
                                                 Core_Elev, Acc_SemiMajor,
                                                 Acc_SemiMinor, Acc_Orientation, Speed, Heading, Angle, AccelSet_Long, AccelSet_Lat, AccelSet_Vert, 
                                                 AccelSet_Yaw, Brakes_WheelBrakes, Size_Width, Size_Length, Sequence_ID, PointsInfo, PathPrediction_Radius, 
                                                 PathPrediction_Confidence));
        
        InsertCursor.close();
        self.__Connection__.commit();

def main():
    Import = ImportRSU();
    Import.SetupConnction();

    FileName = 'D:/DataSource/ConnectedVehicle/2017_12_5_13_rsu43B.csv';
    Import.ImportRSU(FileName, '43B');
    
if __name__ == '__main__':
    main();