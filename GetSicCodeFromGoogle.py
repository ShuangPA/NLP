#coding: utf8
#author: Shuang Zhao (shuang.zhao11@pactera.com)
'''
Get SIC from google api
'''

import optparse
import time
import pandas as pd
from googleapiclient.discovery import build
import re
from CommonFunc import *

def callApi(input):
  service = build("customsearch", "v1",
                  developerKey="AIzaSyC1o8pJAwMvaRugaRp9nWtvrGQs2_llEps")
  result = service.cse().list(
    q=input,
    cx='005808576341306023160:jqleeblmoyi',
  ).execute()
  return result

def getSicByApi(items, name):
  result1 = {}
  result2 = {}
  for item in items:
    if name in item['snippet'] or nameReplace(name) in item['snippet']:
      possible = re.findall(r'sic code[a-zA-Z]*[^\w]*[0-9]+', item['snippet'],
                     re.IGNORECASE)
      for idx in range(len(possible)):
        num = re.findall(r'[0-9]+', possible[idx])
        if len(num[0]) == 4:
          if name in item['snippet'] or nameReplace(name) in item['snippet']:
            if num[0] in result1.keys():
              result1[num[0]] += 1
            else:
              result1[num[0]] = 1
          else:
            if num[0] in result2.keys():
              result2[num[0]] += 1
            else:
              result2[num[0]] = 1
  res1 = sorted(result1.items(), key=lambda d: d[1], reverse=True)
  res2 = sorted(result2.items(), key=lambda d: d[1], reverse=True)
  if len(res1) > 0:
    return res1[0][0]
  else:
    if len(res2) > 0:
      return res2[0][0]
    else:
      return 'None'

if __name__ == '__main__':
  usage = "usage: %prog [options]"
  parser = optparse.OptionParser(usage=usage)
  parser.add_option("--input", default="US_company_info_list(with_SIC).csv",
                    help='input of company info list with SIC code')
  parser.add_option("--output", default="US_company_info_list(SIC_by_Api).csv",
                    help='output of the expanded company list with SIC code '
                         'extracted form Google search')
  (options, args) = parser.parse_args()

  df = pd.read_csv(options.input, header=None, sep=',')
  allSymbol = list(df[0][1:])
  allName = list(df[1][1:])
  allSic = list(df[2][1:])
  allSector = list(df[3][1:])
  allIndustry = list(df[4][1:])
  newSic = []
  question = 'sic code of '
  for idx in range(len(allSic)):
    if allSic[idx] == 'None':
      temp = callApi(question + allName[idx])
      items = temp['items']
      snip = ''
      for item in items:
        snip += item['snippet']
      print(allName[idx])
      newSic.append(getSicByApi(items, allName[idx]))
      time.sleep(0.5)
    else:
      newSic.append(allSic[idx])
    print(idx)
  output = pd.DataFrame(data = {'symbol':allSymbol, 'name':allName,
                                'SICcode':newSic, 'sector':allSector,
                                'industry':allIndustry},
                        columns = ['symbol', 'name', 'SICcode',
                                   'sector', 'industry'])
  output.to_csv(options.output, index = False, sep=',')
