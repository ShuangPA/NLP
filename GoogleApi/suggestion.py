#coding: utf8
#author: Shuang Zhao (shuang.zhao11@pactera.com)
'''
Get google suggestions
'''
import optparse
import requests
import json

def getSuggestions(input):
  tail = f'{input} vs'
  URL="http://suggestqueries.google.com/complete/search?client=firefox&q=" \
      + tail
  headers = {'User-agent':'Pingan/5.0'}
  response = requests.get(URL, headers=headers)
  result = json.loads(response.content.decode('latin-1'))
  return result
if __name__ == '__main__':
  usage = "usage: %prog [options]"
  parser = optparse.OptionParser(usage=usage)
  parser.add_option("--input", default="Apple",
                    help='input name')
  (options, args) = parser.parse_args()

  suggestions = getSuggestions(options.input)
