#coding: utf8
#author: Shuang Zhao (shuang.zhao11@pactera.com)
'''
Merge three listed companies, only keep useful information
'''
import optparse
import pandas as pd
from CommonFunc import *

if __name__ == '__main__':
  usage = "usage: %prog [options]"
  parser = optparse.OptionParser(usage=usage)
  parser.add_option("--output1", default="company_name_list.txt",
                    help='output of company list')
  parser.add_option("--output2", default="US_company_info_list.csv",
                    help='output of company information')
  (options, args) = parser.parse_args()

  df1=pd.read_csv('data/company_NASDAQ.csv', header=None, sep=',')
  df2=pd.read_csv('data/company_NYSE.csv', header=None, sep=',')
  df3=pd.read_csv('data/company_AMEX.csv', header=None, sep=',')

  allSymbol = list(df1[0][1:]) + list(df2[0][1:]) + list(df3[0][1:])
  allName = list(df1[1][1:]) + list(df2[1][1:]) + list(df3[1][1:])
  allSector = list(df1[5][1:]) + list(df2[5][1:]) + list(df3[5][1:])
  allIndustry = list(df1[6][1:]) + list(df2[6][1:]) + list(df3[6][1:])
  out = pd.DataFrame(data = {'symbol':allSymbol, 'name':allName,
                             'sector':allSector, 'industry':allIndustry},
                     columns = ['symbol', 'name', 'sector', 'industry'])
  out.to_csv(options.output2, index=False, sep=',')

  justCompany = list(set(allName))
  for i in range(len(justCompany)):
    justCompany[i] = justCompany[i].lower()
  saveFile(justCompany, options.output1)