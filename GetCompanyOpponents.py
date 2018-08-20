#coding: utf8
#author: Shuang Zhao (shuang.zhao11@pactera.com)
'''
Get companies' opponents by Google suggestion.
Can be used to expand company lists
Need to filter the result(only keep company names)
'''
import optparse
import time
import random
import pandas as pd
from CommonFunc import *
from GoogleApi.GetSuggestion import *

if __name__ == '__main__':
  usage = "usage: %prog [options]"
  parser = optparse.OptionParser(usage=usage)
  parser.add_option("--input", default="company_name_list.txt",
                    help='input of company list')
  parser.add_option("--output1", default="companyOpponentsAll.txt",
                    help='output of all possible company opponents')
  parser.add_option("--output2", default="companyExpandedList.txt",
                    help='output of the expanded company list')
  (options, args) = parser.parse_args()

  companyList = readFile(options.input)
  companyListString = str(companyList)
  print(f'length of companies list: {len(companyList)}')
  results = {}
  count = 1
  print('suggestions fetch begin:')
  for company in companyList:
    tail1 = company.replace('&','and')
    tail2 = nameReplace(company.replace('&','and'))
    allSuggestion = \
      list(set(getSuggestions(tail1)[1] + getSuggestions(tail2)[1]))
    outputTemp = []
    for item in allSuggestion:
      itemSplit =\
        [item.split(' vs ',1), item.split(' vs ',1), item.split(' vs ',1)]
      for idx in range(3):
        if len(itemSplit[idx]) == 2:
          outputTemp.append(itemSplit[idx][1])
    results[company] = list(set(outputTemp))
    print(count)
    count += 1
    sleepTime = random.uniform(0, 1)
    time.sleep(sleepTime)
    if count % 100 == 0:
      time.sleep(5)
  print('suggestions fetch over')
  saveDictToCSV(results, options.output1)
  nextList = companyList
  for company in results:
    for oppo in results[company]:
      if oppo not in companyListString:
        nextList.append(oppo)
  nextList = list(set(nextList))
  for idx in range(len(nextList)):
    nextList[idx] = nextList[idx].lower()
  print(f'length of new company list: {len(nextList)}')
  saveFile(nextList, options.output2)
