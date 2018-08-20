#coding: utf8
#author: Shuang Zhao (shuang.zhao11@pactera.com)

def nameReplace(input):
  return input.lower().replace(' corp. ', ' ').replace(' corp ', ' ')\
    .replace(' co. ', ' ').replace(' co ', ' ').replace(', inc. ', ' ')\
    .replace(', inc ', ' ').replace(' inc. ', ' ').replace(' inc ', ' ')

def saveFile(data, filename):
  outputFile = open(filename, 'w')
  outputFile.write(str(data))
  outputFile.close()

def readFile(filename):
  inputFile = open(filename, 'r').readlines()
  return eval(inputFile[0])

def saveDictToCSV(data, filename):
  outputFile = open(filename, 'w')
  for key in data:
    outputFile.write(str(key) + ': ' + str(data[key]) + '\n')
  outputFile.close()
