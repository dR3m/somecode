from hashlib import md5, sha256
import re
import os
import random

class RuleBuilder:

  def __init__(self, dirPath, fileName, params):
    self.dirPath = dirPath
    self.fileName = fileName
    self.filePath = self.dirPath + self.fileName

    self.params = dict()
    self.parseParams(params)

    self.MD5 = self.getMD5(self.filePath)
    self.SHA256  = self.getSHA256(self.filePath)  

    self.WhiteList = []
    self.loadCriteries()

    self.asciiList = []
    self.unicodeList = []
    self.linksList = []
    self.getStringsFromBin(self.filePath)

    print 'init: OK'
   
  def parseParams(self, params):
    for p in params:
      pname, pval = p.split(':')
      self.params.setdefault(pname, pval)  

  def getFiles(self):
    return os.listdir(self.dirPath)

  def getMD5(self, path):
    f = open(path, 'rb')
    h = md5()
    for line in f.readlines():
        h.update(line)
    f.close()
    return h.hexdigest() 

  def getSHA256(self, path):
    f = open(path, 'rb')
    h = sha256()
    for line in f.readlines():
        h.update(line)
    f.close()    
    return h.hexdigest() 

  def getStringsFromBin(self, path):
    f = open(path, 'rb').read()

    asciiChars = r'[0-9a-zA-Z/\\\-:;\.,_$%@\'()\{\}\[\]<> ]{6,100}'
    regExpAscii = re.compile(asciiChars)
    asciiList = regExpAscii.findall(f)
    asciiList = list(set(asciiList))

    unicodeChars = ur'(?:[\x20-\x7E][\x00]){6,100}'
    regExpUnicode = re.compile(unicodeChars,re.UNICODE)
    unicodeList = regExpUnicode.findall(f)
    unicodeList = list(set(unicodeList))

    linksList = []
    copyList = asciiList
    for s in copyList:
      if 'http' in s:
        linksList.append(s)
        asciiList.remove(s)

    self.asciiList = asciiList
    self.unicodeList = unicodeList
    self.linksList = linksList  
    #return (asciiList, unicodeList, linksList)

  def loadCriteries(self):
    f = open('WL1.txt', 'r')
    for s in f.readlines():
      tmp = s
      if '\n' == tmp[-1]:
        tmp = tmp[0:-1]
      self.WhiteList.append(tmp)
    f.close()

    f = open('WL2.txt', 'r')
    for s in f.readlines():  
      tmp = s
      if '\n' == tmp[-1]:
        tmp = tmp[0:-1]
      self.WhiteList.append(tmp)
    f.close()   

  # Check is string is malicious
  def StrIsBad(self):
    tmp = []
    for s in self.asciiList:
      if s not in self.WhiteList:
        tmp.append(s)
    self.asciiList = tmp

    tmp = []
    for s in self.unicodeList:
      if s not in self.WhiteList:
        tmp.append(s)
    self.unicodeList = tmp

    tmp = []
    for s in self.linksList:
      if s not in self.WhiteList:
        tmp.append(s)
    self.linksList = tmp

    print 'StrIsBad: OK'

  #randomly reduce number of strings  
  def RandomReduceRows(self, n):
    tmp = []
    if len(self.asciiList) > n:
      for i in range(n):
        tmp.append(random.choice(self.asciiList))
    self.asciiList = tmp

    tmp = []
    if len(self.unicodeList) > n:
      for i in range(n):
        tmp.append(random.choice(self.unicodeList))
    self.unicodeList = tmp

  def CMPwithOthers(self):
    for n in self.getFiles():
      if n != self.fileName:
        print 'Comparing with ', n
        b = RuleBuilder(self.dirPath, n, [])
        tmp = []
        for s1 in self.asciiList:
          for s2 in b.asciiList:
            if s2.find(s1) != -1:
              tmp.append(s1)
        self.asciiList = list(set(tmp))

        tmp = []
        for s1 in self.unicodeList:
          for s2 in b.unicodeList:
            if s2.find(s1) != -1:
              tmp.append(s1)
        self.unicodeList = list(set(tmp))

    print 'CMPwithOthers: OK'

  def EscapeChrs(self):
    for i in range(len(self.asciiList)):
      self.asciiList[i] = self.asciiList[i].replace('\\', '\\\\')
      self.asciiList[i] = self.asciiList[i].replace('\"', '\\\"') 

    self.unicodeList = [''.join(s.split(b'\x00')) for s in self.unicodeList]      
    for i in range(len(self.unicodeList)):
      self.unicodeList[i] = self.unicodeList[i].replace('\\', '\\\\') 
      self.unicodeList[i] = self.unicodeList[i].replace('\"', '\\\"') 

  def BuldRule(self):
    self.EscapeChrs()

    name = self.params['malname']
    f = open( name + '.yar', 'w')
    f.write('rule '+ name + ':' + self.params['maltype']+'\n')
    f.write('{\n')
    
    f.write('\tmeta:\n')
    for p in self.params:
      f.write('\t\t' + p + ' = \"' + self.params[p] + '\"\n')
    f.write('\t\tmd5sum = \"' + self.MD5 + '\"\n')
    f.write('\t\tsha256sum = \"' + self.SHA256 + '\"\n')
    
    f.write('\tstrings:\n')
    c = 0
    for s in self.asciiList:
      f.write('\t\t$s' + str(c) + ' = \"'+ s + '\" nocase\n')
      c += 1

    for s in self.unicodeList:
      f.write('\t\t$s' + str(c) + ' = \"' + s + '\" wide nocase\n')
      c += 1

    for s in self.linksList:
      f.write('\t\t$s' + str(c) + ' = \"' + s + '\" nocase\n')
      c += 1

    f.write('\tcondition:\n\t\tall of them\n')
    f.write('}\n')    
    f.close()

    print name + '.yar rule created.'

def main():
  dirPath = 'samples/rat/'
  fileName = 'DarkComet.exe.sample'
  
  s =  RuleBuilder(dirPath, fileName, ['maltype:RAT', 'malname:DarkComet']) 
  s.StrIsBad()
  s.CMPwithOthers()
  #s.RandomReduceRows(20)
  s.BuldRule()

if __name__ == "__main__":	
	main()