# coding: utf8

import sys
import re
import math

import apriori


arrAll=[]
arrObe =[]
testLine = raw_input()
arr =testLine.strip().split()
userID = arr[0]
downloadRes =arr[1]
if downloadRes:
    #arrObe.append(downloadRes.strip().split(','))
    arrAll.append(downloadRes.strip().split(','))
collectionRes =arr[2]
if collectionRes:
    arrAll.append(collectionRes.strip().split(','))
scoreRes = arr[3]
if scoreRes:
    arrAll.append(scoreRes.strip().split(','))
arr4=arr[4]
if arr4:
    arrAll.append(arr4.strip().split(','))
arr5=arr[5]
if arr5:
    arrAll.append(arr5.strip().split(','))
dataSet = arrAll
print 'dataSet: ', dataSet

    # Apriori 算法生成频繁项集以及它们的支持度
    # 这个
L1, supportData1 = apriori.apriori(dataSet, minSupport=0.2)
print 'L(0.7): ', L1
print 'supportData(0.7): ', supportData1

    # 生成关联规则
dic = dict()
rules = apriori.generateRules(L1, supportData1, minConf=0.8)
print 'rules: ', rules[:10]
print type(rules)

#for i in range(0,len(rules)):
 #   if rules[i][0]==frozenset(['58691ed3d87f49b489feb40de28a92f9']):
  #      print map(str,rules[i][1])
   #     dic[map(str,rules[i][0])].append(map(str,rules[i][1]))
    #    print dic

"""
for line in sys.stdin:
    arr =line.strip().split()
    userID = arr[0]
    downloadRes =arr[1]
    if downloadRes:
        arrAll.append(downloadRes.strip().split(','))
    collectionRes =arr[2]
    if collectionRes:
        arrAll.append(collectionRes.strip().split(','))
    scoreRes = arr[3]
    if scoreRes:
        arrAll.append(scoreRes.strip().split(','))
    print arrAll
"""