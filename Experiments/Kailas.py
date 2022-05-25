# -*- coding: utf-8 -*-
"""
Created on Mon May 23 12:46:46 2022

@author: tonum
"""

import PyPDF2
import re
import textract   
import warnings
import pandas as pd
from collections import namedtuple
warnings.filterwarnings("ignore",category=DeprecationWarning)


pdf_file = open(r"C:\Users\Oracle\Downloads\2022_05_17_20_21_01.pdf", 'rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
number_of_pages = read_pdf.getNumPages()
pdf = []
for i in range(number_of_pages):
    page = read_pdf.getPage(i)
    page_content = page.extractText()
    page_content
    pdf.extend(page_content.split('\n'))
pdf1 = pdf[23:7624]

print(pdf1)

def extracttransaction(pdf):
    str1 = ''
    for i in pdf:
        if type(i)==str and '/' in i:
            str1 += i
            pdf.remove(i)
        else:
            str1 += ','
    str1
    list2 = re.sub(',+',',',str1)
    list3 = list2.split(',')
    print(len(list3))
    return list3


extracttransaction(pdf1)


tran_id = []
for i,string in enumerate(pdf1):
    count = 0
    try:
        if '/' in string and count == 0 :
            count += 1
            tran_id.append(string)
        elif '/' in string and count > 1:
            del string
    except:
        count = 0
print((tran_id))

str2 = []
list1= list('abcdefghijklmnopqrstuvwxyz/MAYKAILAS')
for i in pdf1:
#     print(i)
    for j in i:
        if j in list1:
            break
    else:
        str2.append(i)

count = 0
list9 = []
for i in str2:
    list9.append(str2[count:(count+6)])
    count += 6
list9

print(list1)

d = {'TR':lll}
print(d)


strz = []
for i in pdf1:
    if type(i)==str and '/' in i:
        pass
    else:
        strz.append(i)
strz
# list2 = re.sub(',+',',',str1)
# list3 = list2.split(',')
# print(len(list3))


re.findall('[0-9]{2}[-][0-9]{2}[-][0-9]{4}',ss)