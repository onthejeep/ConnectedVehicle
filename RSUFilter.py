import shapely.geometry;
import shapefile;
import pandas as pan;
import xmltodict;
import csv;
import os.path;
import IDEncryption;

class Filter:
    def __init__(self, psid, payloadType):
        self.__StudyAreaFileName__ = 'data/StudyArea.shp';
        self.PSID = psid;
        self.PayloadType = payloadType;

    def ReadStudyArea(self):
        '''
        Read study area (in shapefile)
        '''
        StudyArea = shapefile.Reader(self.__StudyAreaFileName__);
        SingleFeature = StudyArea.shapeRecords()[0];
        Polygon_Binary = SingleFeature.shape;
        Polygon_Geom = shapely.geometry.shape(Polygon_Binary);
        
        return(Polygon_Geom);

    def Filter_GeoFence(self, polygon, longitude, latitude):
        ''' 
        wheather a point is located in a polygon
        return: true/false
        '''
        GPS_Point = shapely.geometry.Point(longitude, latitude);
        Result = GPS_Point.within(polygon);
        return(Result); 

    def Execute(self):
        pass;


class SpatFilter(Filter):

    def __init__(self):
        super().__init__('32770', 'spat');

 
    def Execute(self, fileName):
        '''
        spat message filter with multiple filters
        '''
        StudyPolygon = self.ReadStudyArea();

        FilteredFileName = 'filtered/{}/{}'.format(self.PayloadType, os.path.basename(fileName));

        with open(FilteredFileName, 'w+', newline = '') as fout:
            with open(fileName, 'r')  as fin:
                Sw = csv.writer(fout);

                for Row in csv.reader(fin):

                    PSID = Row[2].strip();
                    if PSID != self.PSID:
                        continue;
                    
                    Sw.writerow(Row);

class BsmFilter(Filter):

    def __init__(self):
        super().__init__('32', 'bsm');
 
    def Execute(self, fileName):
        '''
        BSM message filter with multiple filters
        '''
        StudyPolygon = self.ReadStudyArea();

        FilteredFileName = 'filtered/{}/{}'.format(self.PayloadType, os.path.basename(fileName));

        with open(FilteredFileName, 'w+', newline = '') as fout:
            with open(fileName, 'r')  as fin:
                Sw = csv.writer(fout);

                for Row in csv.reader(fin):

                    PSID = Row[2].strip();
                    if PSID != self.PSID:
                        continue;

                    BSM = Row[3];
                    BSM_Xml = xmltodict.parse(BSM);
                    Latitude = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['lat']) / 1e7;
                    Longitude = float(BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['long']) / 1e7;
                    if not self.Filter_GeoFence(StudyPolygon, Longitude, Latitude):
                        continue;

                    Core_ID = BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['id'];
                    EncodedID = IDEncryption.IDEncryption.EasyEncode(Core_ID);

                    BSM_Xml['MessageFrame']['value']['BasicSafetyMessage']['coreData']['id'] = EncodedID;
                    Row[3] = xmltodict.unparse(BSM_Xml, full_document = False);

                    Sw.writerow(Row);
            
def main():
    Bsm_Filter = BsmFilter();
    Spat_Filter = SpatFilter();
    DirectoryPath = 'D:/DataSource/ConnectedVehicle/original';

    for fileName in os.listdir(DirectoryPath):
        FilePath = os.path.join(DirectoryPath, fileName);
        print('processing {}'.format(FilePath));

        Bsm_Filter.Execute(FilePath);
        Spat_Filter.Execute(FilePath);
    
if __name__ == '__main__':
    main();

    #IDEncryption.IDEncryption.SaveKey();

    #EnMessage = IDEncryption.IDEncryption.Encode(tempID = 'shuyang'.encode());
    #print(EnMessage.decode());

    #DeMessage = IDEncryption.IDEncryption.Decode(decodedID = EnMessage);
    #print(DeMessage.decode());

    

    #print(IDEncryption.IDEncryption.EasyEncode('45serd'));

    


