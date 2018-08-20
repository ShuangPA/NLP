#coding: utf8
#author: Shuang Zhao (shuang.zhao11@pactera.com)
'''
Extract company information from Wikipedia. The information are founders,
key people, products, parent, subsidiaries.

Problem: Some of the company information are not separated into list
(May need to be solved)
'''
import optparse
import requests
import bs4
from googleapiclient.discovery import build

def getWikiTable(companyName):
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
                  developerKey="AIzaSyC1o8pJAwMvaRugaRp9nWtvrGQs2_llEps")
  result = service.cse().list(
      q=companyName,
      cx='005808576341306023160:cnbbimkz8d0',
      num=1
  ).execute()
  link = result['items'][0]['link']
  response = requests.get(link)
  soup = bs4.BeautifulSoup(response.content, 'lxml')
  table = soup.find('table', {'class': 'infobox'})
  rows = table.find_all('tr')[2:]
  infoDict = dict()
  for row in rows:
      children = row.findChildren(recursive=False)
      row_text = []
      for child in children:
          cleanText = child.text
          cleanText = cleanText.strip()
          cleanText = cleanText.split('\n')
          if not row_text:
              key = cleanText[0]
          else:
              infoDict[key] = cleanText
          row_text.append(cleanText)
  output = {}
  wantList = ['Founders', 'Key people', 'Products', 'Parent', 'Subsidiaries']
  for item in wantList:
      if item in infoDict.keys():
          output[item] = infoDict[item]
  return output
if __name__ == '__main__':
  usage = "usage: %prog [options]"
  parser = optparse.OptionParser(usage=usage)
  parser.add_option("--input", default="Apple",
                    help='company name')
  (options, args) = parser.parse_args()
  result = getWikiTable(options.input)