# -*- coding: utf-8 -*-

import sys
import  re
import  math


rownum =1
"""
select score,down_count,collected_count,comment_count,view_count,product_code,      6
       product_name,year,month,day,times,     11
       classification_id,classification_name    13
    from zshtest

 """
try:
    for line in sys.stdin:
        arr = line.strip().split()
        score = float(arr[0])
        down_count = float(arr[1])
        collected_count = float(arr[2])
        comment_count = float(arr[3])
        view_count   = float(arr[4])
        print arr
        if(score < 0):
            score = 0
        if ( view_count> 0 and rownum!=1   ):
            try:
                if (arr[10]):
                    times = float(arr[10])
                    rank = int(score + (down_count+collected_count+comment_count+times)/view_count)
                else:
                    rank = int(score + (down_count+collected_count+comment_count)/view_count)
            except:
                rank = 0
        else:
            if(rownum ==1 ):
                rank =30
            else:
                rank = 0
        if (rank>20):
            print ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (rank,arr[5],arr[6],arr[7],arr[8],arr[9],arr[10],arr[11],arr[12]))
        rownum +=1
except:
    pass