#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import codecs

alf = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ_'
N = 31

def index_coincidence(t):
    n = len(t)
    indx = {}
    for i in alf:
        for j in t:
            if i == j:
                if indx.get(i) == None:
                    indx[i] = 1
                else:
                    indx[i] = indx[i]+1
    I = 0
    for i in indx.keys():
        I = I + (indx[i]*(indx[i]-1)/(n*(n-1)))
    return I      
     
def find_period(text, f):
    I = 0
    L_KEY = 0
    f.write('поиск периода\n')
    f.write('_____________________________________\n')
    for len_key in range(5, 12) :
        tmp1 = [text[shift::len_key] for shift in range(len_key)]
        tmp2 = sum([index_coincidence(t) for t in tmp1 ])/len_key
        f.write(str(tmp2)+' '+str(len_key)+'\n') #'{0:f}.format(tmp2)'
        if round(tmp2, 4) > I: 
            I = round(tmp2, 4) 
            L_KEY = len_key
    print('Длина ключа:', L_KEY)
    return L_KEY

def dec(text, p):
    res = ''
    for i in text:
        res = res + alf[(alf.find(i)+p)%N]
    return res    

def chi_square(text):
    E = {'_':0.175, 'О':0.10983, 'Е':0.08496, 'А':0.07998, 'И':0.08574 , 'Н':0.067, 'Т':0.06318, 'С':0.05473, 'Р':0.04746, 'В':0.04533, 'Л':0.04343, 'К':0.03486, 'М':0.03203, 'Д':0.02977, 'П':0.02804, 'У':0.02615, 'Я':0.02001, 'Ы':0.01898, 'Ь':0.01772, 'Г':0.01687, 'З':0.01641, 'Б':0.01592, 'Ч':0.0145, 'Х':0.00966, 'Ж':0.0094, 'Ш':0.00718, 'Ю':0.00639, 'Ц':0.00486, 'Щ':0.00361, 'Э':0.00331, 'Ф':0.00267, }
    frec = {}
    n = len(text)
    for i in alf:
        for j in text:
            if i == j:
             if frec.get(i) == None:
                 frec[i] = 1
             else:
                frec[i] = frec[i]+1
    res = 0
    for i in frec.keys():
        res = res + ((frec[i]/n-E[i])**2)/E[i]
    return res
        
def main():
    text = ''
    f = codecs.open('output.txt', 'r', 'cp1251')
    for line in f.readlines():
            text = text+line.replace('\n','').replace('\r','')
    f.close()
    f = codecs.open('statistic.txt', 'w', 'utf-8')
    
    KEY_LEN = find_period(text, f)
    KEY_DIGIT = [0 for i in range(KEY_LEN)] 
    res = []
    f.write('поиск ключа\n')
    f.write('_____________________________________\n')
    f.write('n-группы  n-сдвига  хи-квадрат\n')
    for k in range(KEY_LEN):
        a = 999999
        s = 0
        for i in range(N):
            tmp =  chi_square(dec(text[k::KEY_LEN], i))
            f.write(str(k)+' '*10+str(i)+' '*10+str(tmp)+'\n')
            if a > tmp: 
                a, s = tmp, i
        KEY_DIGIT[k] = s
        res.append(dec(text[k::KEY_LEN], s))
    
    dec_text = ''
    while True:
        if '' in res: break
        for i in range(KEY_LEN):
            dec_text = dec_text + res[i][0]
            res[i] = res[i][1:] 
    KEY_DEC = ''.join([alf[i] for i in KEY_DIGIT])
    KEY_ENC = ''.join([alf[(N-i)%N] for i in KEY_DIGIT])
    f.write('Ключ расшифрования:'+KEY_DEC+'\n')
    f.write('Ключ шифрования:'+KEY_ENC+'\n')
    f.write('\nРасшифрованный текст\n')
    f.write(dec_text)    
    print('Ключ шифрования:',KEY_ENC)      
    print(KEY_DIGIT)
    f.close()

if __name__ == '__main__':
    main()