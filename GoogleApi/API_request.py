#coding: utf8
#author: Shuang Zhao (shuang.zhao11@pactera.com)
'''
Get all results from google
'''
import optparse
from googleapiclient.discovery import build

def callApi(input):
  service = build("customsearch", "v1",
                  developerKey="AIzaSyC1o8pJAwMvaRugaRp9nWtvrGQs2_llEps")
  result = service.cse().list(q=input, cx='005808576341306023160:cnbbimkz8d0')\
    .execute()
  return result
if __name__ == '__main__':
  usage = "usage: %prog [options]"
  parser = optparse.OptionParser(usage=usage)
  parser.add_option("--input", default="Apple",
                    help='input search item')
  (options, args) = parser.parse_args()
  result = callApi(options.input)
