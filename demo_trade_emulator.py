

import os
from random import randint
import json
import time

from TradeEmulator.companies_list import SYMBOLS, NAMES, INDUSTRY

MIN_QUANTITY = 4000
MAX_QUANTITY = 10000
# DEFAULT_QUANTITY = 10000
tradeEmulatorDir = 'C:/CodeWeek/TradeEmulator/Positions'

def main():
    """
    Entry point, emulates trade activity by adding and removing positions to the store at random time intervals
    :return:
    """
    createDirectoriesIfDirectoriesDontExist(tradeEmulatorDir)
    while 1:
        time.sleep(randint(2, 5))
        if len(os.listdir(tradeEmulatorDir)) < 50:
            quantity = randint(MIN_QUANTITY, MAX_QUANTITY)
            if addPosition(quantity, tradeEmulatorDir) == -1:
                break
        elif len(os.listdir(tradeEmulatorDir)) > 200:
            pass
        else:
            addOrRemove = randint(0,1)
            if addOrRemove:
                quantity = randint(MIN_QUANTITY, MAX_QUANTITY)
                if addPosition(quantity, tradeEmulatorDir) == -1:
                    break
            else:
                if removePosition(tradeEmulatorDir) == -1:
                    break

    return




def createDirectoriesIfDirectoriesDontExist(fullpath=None):
    """
    Self explanatory
    :param fullpath: full path of directory you wish to create
    :return:
    """
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)
        print('{} successfully created...'.format(fullpath))
    else:
        print('{} already exists...'.format(fullpath))


def addPosition(quantity, root):
    """
    :param quantity: size(in GBP) of the position
    :param root: root directory to positions
    :return: 0 if successful, -1 if not
    """
    if os.path.exists(root):
        positions = os.listdir(root)
        while 1:
            assetID = str(randint(10000000, 99999999))
            if assetID not in positions:
                break
        with open('{}/{}.json'.format(root, assetID), 'w') as f:
            companyIdx = randint(0, len(SYMBOLS) - 1)
            posDict = {}
            posDict['Symbol'] = SYMBOLS[companyIdx]
            posDict['CompanyName'] = NAMES[companyIdx]
            posDict['Industry'] = INDUSTRY[companyIdx]
            posDict['Quantity'] = quantity
            json.dump(posDict, f)
        return 0

    else:
        print('Positions directory does not exist, quitting...')
        return -1


def removePosition(root):
    """
    :param root: root directory to positions
    :return: 0 if successful, -1 if not
    """
    if os.path.exists(root):
        positions = os.listdir(root)
        idxToRemove = randint(0, len(positions) - 1)
        os.remove('{}/{}'.format(root, positions[idxToRemove]))
        return 0

    else:
        print('Positions directory does not exist, quitting...')
        return -1


if __name__ == "__main__":
    main()