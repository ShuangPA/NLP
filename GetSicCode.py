#coding: utf8
#author: Shuang Zhao (shuang.zhao11@pactera.com)
'''
Get SIC code of companies from Nasdap stockreports
'''
import optparse
import pandas as pd
import requests
import bs4

def getSic(name):
  url = 'https://stockreports.nasdaq.edgar-online.com/' + name + '.html'
  response = requests.get(url)
  soup = bs4.BeautifulSoup(response.content, 'lxml')
  code = soup.find('span', {'id': 'lblSICCode'}).get_text()
  return code

if __name__ == '__main__':
  usage = "usage: %prog [options]"
  parser = optparse.OptionParser(usage=usage)
  parser.add_option("--input", default="US_company_info_list.csv",
                    help='input of company information list')
  parser.add_option("--output", default="US_company_info_list(with_SIC).csv",
                    help='output of company information list with SIC code')
  (options, args) = parser.parse_args()

  df=pd.read_csv(options.input, header=None, sep=',')
  allSymbol = list(df[0][1:])
  allName = list(df[1][1:])
  allSector = list(df[2][1:])
  allIndustry = list(df[3][1:])
  sic = []
  for idx in range(len(allSymbol)):
    try:
      code = getSic(allSymbol[idx])
      if code == '':
        code = 'None'
    except:
      code = 'None'
    sic.append(code)
    print(idx)
  output = pd.DataFrame(data = {'symbol':allSymbol, 'name':allName,
                                'SICcode':sic, 'sector':allSector,
                                'industry':allIndustry},
                        columns = ['symbol', 'name', 'SICcode',
                                   'sector', 'industry'])
  output.to_csv('US_company_info_list(with_SIC).csv', index = False, sep=',')
