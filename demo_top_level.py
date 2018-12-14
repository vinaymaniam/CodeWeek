



import time
import json

from news_connect import newsByCompanyName, getDictionaries, getSentiment, aggregate

from positions_aggregator import aggregatePositions, posListToPosDict
from TradeEmulator.companies_list import NAMES, SYMBOLS

import re

def main():
    generateOutput()
    print('Done')


def generateOutput():
    companyLookup = {symbol: name for symbol, name in zip(SYMBOLS, NAMES)}
    symbolLookup = {name: symbol for symbol, name in zip(SYMBOLS, NAMES)}
    t1 = time.time()

    aggregatedPositions = aggregatePositions(publishToFile=False)
    top20PositionsList = aggregatedPositions  # [:20]
    top20Positions = posListToPosDict(top20PositionsList)

    top20CompanyNames = [companyLookup[symbol[0]] for symbol in top20Positions.items()]
    top20CompanyNames = cleanCompanyNames(top20CompanyNames)
    news = newsByCompanyName(top20CompanyNames, 1)
    dictionaries = getDictionaries()
    dictionaryToUse = dictionaries['positive']  # TODO: we can explore using both the positive and negative dictionary

    enrichedData = enrichPosDict(top20Positions, top20PositionsList, news, dictionaryToUse, companyLookup)

    t2 = time.time()
    print('Process took {} seconds'.format(t2 - t1))
    with open('BackendOutput/output.json', 'w') as outfile:
        json.dump(enrichedData, outfile)
        print('File successfully generated')


def cleanCompanyNames(companyNames, badWords=('inc', 'corp', 'ltd', '.', ',')):
    """
    Remove unnecessary words which damage the keyword search such as Inc. Ltd. Corp.
    :param companyNames: List of company names
    :param badWords: List of words to remove
    :return:
    """

    for badWord in badWords:
        bw = re.compile(re.escape(badWord), re.IGNORECASE)
        companyNames = [bw.sub('', cn).strip() for cn in companyNames]
        # companyNames = [cn.replace(badWord, '') for cn in companyNames]

    return companyNames


def enrichPosDict(posDict, posList, news, dictToUse, companyLookup):
    """
    :param posDict: dictionary of symbol : quantity pairs aggregated from all positions we hold
    :return: enriched dict, containing the above + rank(by position),  company name, article headlines, sources,
             sentiments, urls
    """
    enrichedData = {}

    for key, value in posDict.items():
        companyName = companyLookup[key]
        if companyName not in news:
            continue
        outObj = {}
        outObj['money'] = value
        outObj['rank'] = getRank(key, posList)
        outObj['company_name'] = companyName
        for article in news[companyName]:
            sentiment = getSentiment(article['title'], dictToUse)
            if sentiment > 0:
                article['sentiment'] = 1
            else:
                article['sentiment'] = 0

        outObj['articles'] = news[companyName]

        enrichedData[key] = outObj

    return enrichedData


def getRank(key, lookup):
    """
    get the rank by size of position
    :param key:
    :param lookup:
    :return:
    """
    for i in range(len(lookup)):
        if lookup[i][0] == key:
            return i


if __name__ == "__main__":
    main()
