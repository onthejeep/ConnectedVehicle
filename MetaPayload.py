import xmltodict;
import csv;
import os.path;
import os;
import json;
import datetime;

class BsmMetaStructure:

    schemaVersion = 1;
    recordGeneratedBy = 'OBU';
    recordGeneratedAt = None;
    logFileName = '';
    logFileSize = 0; # in kb
    payloadType = 'BsmPayload';
    recordType = '';
    serialId_bundledId = 0;
    serialId_recordId = 0;
    bsmSource = 'CV';
    securityResultCode = 'unknown';

    def __init__(self):
        pass;

# 32: BSM
# 32770: SPAT


class BsmMeta:
    def __init__(self):
        self.PSID = '32';
        self.PayloadType = 'bsm';
        self.Meta = {};
        pass;

    def Execute(self, fileName, metaDirectory):

        FilteredFileHandle = open(fileName, 'r');
        CsvReader = csv.reader(FilteredFileHandle);
        FilteredFileInfo = os.stat(fileName);
        FileSize = FilteredFileInfo.st_size;
        FileName = os.path.basename(fileName);
        RowCount = sum(1 for row in open(fileName));

        RowIndex = 1;
        for timestamp, kind, type, message in CsvReader:

            MetaFileName = '{}/meta/{}/{}_{}.json'.format(metaDirectory, self.PayloadType, os.path.splitext(FileName)[0], RowIndex);

            Meta = {};
            Meta['schemaVersion'] = 1;
            Meta['recordGeneratedBy'] = 'OBU';
            Meta['recordGeneratedAt'] = '{} [ET]'.format(datetime.datetime.fromtimestamp(float(timestamp) / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]);
            Meta['logFileName'] = FileName;
            Meta['logFileSize'] = '{} byte'.format(FileSize); # in byte
            Meta['payloadType'] = 'BsmPayload';
            Meta['recordType'] = 'bsmTx';
            Meta['numRecord'] = RowCount;
            Meta['serialId'] = {};
            Meta['serialId']['bundledId'] = 0;
            Meta['serialId']['recordId'] = RowIndex;
            Meta['bsmSource'] = 'CV';
            Meta['securityResultCode'] = 'unknown';

            RowIndex += 1;

            Bsm_Dict = xmltodict.parse(message);

            Payload = {};
            Payload['dataType'] = 'j2735.J2735Bsm';
            Payload['data'] = {};
            Payload['data']['coreData']= Bsm_Dict['MessageFrame']['value']['BasicSafetyMessage']['coreData'];
            Payload['data']['partII'] = Bsm_Dict['MessageFrame']['value']['BasicSafetyMessage']['partII'];

            Meta_Bsm = {};
            Meta_Bsm['metadata'] = Meta;
            Meta_Bsm['payload'] = Payload;

            with open(MetaFileName, 'w+') as fout:
                fout.write(json.dumps(Meta_Bsm));
            
        FilteredFileHandle.close();


if __name__ == '__main__':
    Meta_Bsm = BsmMeta();
    DirectoryPath = 'C:/DataDownload/Onebusaway/Onebusaway';
    FileName = '{}/filtered/bsm/{}'.format(DirectoryPath, '2017_12_5_13_rsu40.csv');
    Meta_Bsm.Execute(FileName, DirectoryPath);
        