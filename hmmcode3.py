# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 01:08:19 2019

@author: nov28
"""

from __future__ import division
import os
import sys
import numpy as np
import glob
import collections
from collections import Counter, defaultdict
import re
import json
import math

def viterbi(line,tagsdistinct,vocab,emisprob,transprob,firstags,lastags):
    vb=defaultdict(float)
    bb=defaultdict(str)
    
    for s in tagsdistinct:
        if line[0] in vocab:
            vb[s+',0']=firstags[s]*emisprob[line[0]+' / '+s]
        else:
            vb[s+',0']=firstags[s]
        bb[s+',0']='0'
    
    for t in range(1,len(line)):
        for s in tagsdistinct:
            if line[t] in vocab:
                vb[s+','+str(t)]= max([ vb[s1+','+str(t-1)]*transprob[s1+','+s]*emisprob[line[t]+' / '+s] for s1 in tagsdistinct ])
                
                maxval1=max([vb[s2+','+str(t-1)]*transprob[s2+','+s]  for s2 in tagsdistinct])
                 
                temps=[s3 for s3 in tagsdistinct if vb[s3+','+str(t-1)]*transprob[s3+','+s]==maxval1]
                bb[s+','+str(t)]=temps[0]
            else:
                maxval2=max([ vb[s1+','+str(t-1)]*transprob[s1+','+s]  for s1 in tagsdistinct])
                vb[s+','+str(t)]= maxval2
                
                temps=[s2 for s2 in tagsdistinct if vb[s2+','+str(t-1)]*transprob[s2+','+s]==maxval2]
                bb[s+','+str(t)]=temps[0]
                
        
    maxval3=max([ vb[s+','+str(len(line)-1)]*lastags[s]  for s in tagsdistinct])
    vb['qf,'+str(len(line)-1)]=maxval3
    temps=[ s1 for s1 in tagsdistinct if vb[s1+','+str(len(line)-1)]*lastags[s1]==maxval3]
    bb['qf,'+str(len(line)-1)]=temps[0]
    
    
    bp=''
    p1='qf'
    p1=bb[p1+','+str(len(line)-1)]
    bp=  bp+' '+p1
    for ppath in range(len(line)-1,0,-1):
        p1=bb[p1+','+str(ppath)]
        bp= bp + ' '+ p1
    
    finpatht= bp.split(" ")
    finpath=finpatht[1:]
    return finpath[::-1]
    

if __name__=="__main__":
    path=sys.argv[1]
    vit=open('hmmmodel.txt','r',encoding='utf8')
    tempt=vit.readline()
    #tagsdistinct
    temptags=vit.readline()
    tagsdistinct=temptags.split(" ")[:-1]
    
    tempt=vit.readline()
    #vocab
    tempvocab=vit.readline()
    vocab=tempvocab.split(" ")[:-1]
    
    tempt=vit.readline()
    #emission prob
    tempem=vit.readline()
    emisprob=defaultdict(float)
    emisprobt=eval(tempem)
    
    tempt=vit.readline()
    #transprob
    temptp=vit.readline()
    transprob=defaultdict(float)
    transprobt=eval(temptp)
    
    tempt=vit.readline()
    #firstags
    tempfirst=vit.readline()
    firstags=defaultdict(float)
    firstagst=eval(tempfirst)
    
    tempt=vit.readline()
    #lastags
    templast=vit.readline()
    lastags=defaultdict(float)
    lastagst=eval(templast)
    vit.close()
    
    
    for key,val in emisprobt.items():
        emisprob[key]=val
    for key,val in transprobt.items():
        transprob[key]=val
    for key,val in firstagst.items():
        firstags[key]=val
    for key,val in lastagst.items():
        lastags[key]=val
               
    data=[]
    fopen=open(path,'r',encoding='utf8')
    for line in fopen:
        nline=line[:-1]
        tokens=nline.split(" ")
        data.append(tokens)
        #print(tokens[:5])
    fopen.close() 
    
    opfile=open("hmmoutput.txt","w+",encoding='utf8')
    for d in data:
        outputtags=viterbi(d,tagsdistinct,vocab,emisprob,transprob,firstags,lastags)
        newstr=""
        for i in range(len(outputtags)):
            newstr= newstr+' '+d[i]+'/'+outputtags[i]
        newstr=newstr[1:]
        opfile.write(newstr+'\n')
    opfile.close()      
