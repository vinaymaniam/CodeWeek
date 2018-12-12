# Just collects all positions we currently hold and groups them by company

import numpy
import os
import json
from demo_trade_emulator import tradeEmulatorDir

import time

def main():
    t1 = time.time()
    aggPos = aggregatePositions()
    t2 = time.time()
    print('Aggregation process took {} seconds'.format(t2-t1))
    for pos in aggPos:
        print(pos)

    return


def aggregatePositions(root=tradeEmulatorDir, returnType='sorted list'):
    """
    :param root: folder to collect positions from
    :param returnType: 'sorted list' or 'dict'
    :return: list of tuples where the first value is the company symbol and the second is total size(in gbp) of position
    """
    fileNames = os.listdir(root)
    filePaths = [os.path.join(root, fn) for fn in fileNames]

    posDict = {}

    for fp in filePaths:
        with open(fp, 'r') as f:
            jsonStr = f.read()
            jsonDict = json.loads(jsonStr)
            if jsonDict['Symbol'] in posDict:
                posDict[jsonDict['Symbol']] += float(jsonDict['Quantity'])
            else:
                posDict[jsonDict['Symbol']] = float(jsonDict['Quantity'])

    if returnType == 'dict':
        return posDict
    else:
        posList = [[key, val] for key,val in posDict.items()]
        posList = sorted(posList, key=lambda pl:pl[1], reverse=True)
        return posList



if __name__ == "__main__":
    main()