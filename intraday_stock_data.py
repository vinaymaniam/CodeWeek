

import json
from Lib.urllib import request

from datetime import date, datetime, timedelta

import time
import numpy

def main():
    """
    For debugging purposes only
    :return:
    """
    t1 = time.time()
    # data = getStockDataForCompanyBySymbol('MSFT')
    impact = measureImpactOfNewsArticle(datetime(2018,12,11,14,45,0), 'MSFT')
    t2 = time.time()
    print("Process took {} seconds".format(t2-t1))
    print(impact)


def measureImpactOfNewsArticle(timestamp, symbol, impactThreshold=0.01):
    """
    :type timestamp: datetime
    :param timestamp: datetime of the news article
    :param symbol: company market symbol
    :param impactThreshold: relative change beyond which difference is considered notable
    :return: the impact of the news article on the stock price(positive/negative and by how much)
    """
    tsData = getStockDataForCompanyBySymbol(symbol)
    timeWindow = findWindowAroundNewsArticle(timestamp, tsData, windowsize=60) # type: list[datetime]
    windowedKeys = [dt.strftime("%Y-%m-%d %H:%M:%S") for dt in timeWindow]
    windowedStockData = [tsData[key] for key in windowedKeys]

    # Measure impact here
    priorData = [tsData[key] for key in windowedKeys if datetime.strptime(key, "%Y-%m-%d %H:%M:%S") <= timestamp]
    postData = [tsData[key] for key in windowedKeys if datetime.strptime(key, "%Y-%m-%d %H:%M:%S") > timestamp]

    priorPrices = [float(pd['1. open']) for pd in priorData]
    postPrices = [float(pd['1. open']) for pd in postData]

    if (len(priorPrices) == 0) | (len(postPrices) == 0):
        return 0

    # Average before vs average after
    priorAvg = numpy.mean(priorPrices)
    postAvg = numpy.mean(postPrices)

    # Or trend based
    if (priorAvg - postAvg) / priorAvg >= impactThreshold:
        return 1
    elif (postAvg - priorAvg) / priorAvg >= impactThreshold:
        return -1
    else:
        return 0

def findWindowAroundNewsArticle(timestamp, tsData, windowsize):
    """
    :param timestamp: datetime object for the time the news article was published
    :param tsData: time series data from api
    :param windowsize: size of time window(specified in minutes) to get from either side of the news article
    :return:
    """
    datetimes = [datetime.strptime(key, "%Y-%m-%d %H:%M:%S") for key in tsData.keys()]
    windowedTimes = [dt for dt in datetimes if dt > timestamp - timedelta(minutes=windowsize)]
    windowedTimes = [dt for dt in windowedTimes if dt < timestamp + timedelta(minutes=windowsize)]
    return windowedTimes



# Takes about 1.5 seconds. If we are dealing with high traffic then we need to call this conservatively
def getStockDataForCompanyBySymbol(symbol):
    """
    Gets intraday stock data for company given its market symbol
    :param symbol: eg. MSFT
    :return:
    """
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=5min&outputsize=full&apikey=2I36TNHZ8RL4VNGL".format(symbol)
    response = request.urlopen(url)
    data = json.loads(response.read())
    tsData = data["Time Series (5min)"]
    return tsData

if __name__ == "__main__":
    main()