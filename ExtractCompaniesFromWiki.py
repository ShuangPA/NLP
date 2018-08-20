#coding: utf8
#author: Shuang Zhao (shuang.zhao11@pactera.com)
'''
Extract list of companies in the Fortune Global 500 from Wikipedia.
'''
import optparse
import requests
import bs4
from CommonFunc import *

if __name__ == '__main__':
  usage = "usage: %prog [options]"
  parser = optparse.OptionParser(usage=usage)
  parser.add_option("--output", default="all_company.txt",
                    help='output filename')
  (options, args) = parser.parse_args()

  companies = list()
  url = 'https://en.wikipedia.org/wiki/List_of_companies_of_the_United_States'
  response = requests.get(url)
  soup = bs4.BeautifulSoup(response.content, 'lxml')
  for list_tag in soup.find_all('div', {'class': 'div-col'}):
    for tag in list_tag.find_all('a'):
      companies.append(tag.get_text())
  current_companies = companies[:companies.index("Adventure International")]
  for idx in range(len(current_companies)):
    current_companies[idx] = current_companies[idx].lower()
  text = str(current_companies)
  saveFile(text, options.output)
