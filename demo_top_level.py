



import time
import json

from news_connect import newsByCompanyName, getDictionaries, getSentiment, aggregate

from positions_aggregator import aggregatePositions, posListToPosDict
from TradeEmulator.companies_list import NAMES, INDUSTRY, SYMBOLS

import re

def main():
    """
    News collection and analysis entry point for demo
    :return:
    """
    result = {}

    companyLookup = {symbol : name for symbol,name in zip(SYMBOLS, NAMES)}

    t1 = time.time()

    aggregatedPositions = aggregatePositions(publishToFile=False)
    top20PositionsList = aggregatedPositions#[:20]
    top20Positions = posListToPosDict(top20PositionsList)

    top20CompanyNames = [companyLookup[symbol[0]] for symbol in top20Positions.items()]
    top20CompanyNames = cleanCompanyNames(top20CompanyNames)
    news = newsByCompanyName(top20Positions, 1)
    dictionaries = getDictionaries()
    dictionaryToUse = dictionaries['positive']  # TODO: we can explore using both the positive and negative dictionary

    for company in news:
        articles = news[company]

        # can use 'title' or 'description' or 'content'
        sentiments = [getSentiment(article['title'], dictionaryToUse) for article in articles]

        result[company] = {'position': top20Positions[company],
                           'sentiment': aggregate(sentiments),
                           'articles': articles}

    t2 = time.time()
    print('Process took {} seconds'.format(t2 - t1))
    with open('BackendOutput/output.json', 'w') as outfile:
        json.dump(result, outfile)


    # [print('{} : {}'.format(key, value)) for key, value in top20Positions.items()]


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


if __name__ == "__main__":
    main()


def main1():
    result = {}
    top20Positions = {'Apple': 1000, 'Google': 500, 'Berkshire': 100}  # TODO: link this to the trades
    news = newsByCompanyName(top20Positions, 1)
    dictionaries = getDictionaries()
    dictionaryToUse = dictionaries['positive']  # TODO: we can explore using both the positive and negative dictionary

    t1 = time.time()
    for company in top20Positions:
        articles = news[company]['articles']

        # can use 'title' or 'description' or 'content'
        sentiments = [getSentiment(article['title'], dictionaryToUse) for article in articles]

        result[company] = {'position': top20Positions[company],
                           'sentiment': aggregate(sentiments),
                           'articles': articles}

    t2 = time.time()
    print('Process took {} seconds'.format(t2 - t1))
    with open('BackendOutput/output.json', 'w') as outfile:
        json.dump(result, outfile)