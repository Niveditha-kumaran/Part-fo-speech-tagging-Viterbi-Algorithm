# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 00:57:37 2019

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
import io
import codecs

if __name__=='__main__':
    path=sys.argv[1]
    #initialization
    tags=[]
    data=[]
    vocab=[]
    tagsdistinct=[]
    
    fp=open(path, 'r',encoding='utf-8')    
    # fopen=fp.read()
    lines = [line for line in fp.readlines()]
    for l in lines:
        #print(l)
        l=l[:-1]
        tokens=l.split(" ")
        data.append(tokens)
    
    #emis count, tag count
    emiscount=Counter()
    tagcount=Counter()
    for dline in data:
        tempt=[]
        #k+=1
        for t in dline:
            revt=t[::-1]
            sep=revt.index('/')
            tag=revt[:sep][::-1]
            word=revt[sep+1:][::-1]
            tagcount[tag]+=1
            tempt.append(tag)
            if word not in vocab:
                vocab.append(word)
            if tag not in tagsdistinct:
                #print(tag,'line ',k)
                tagsdistinct.append(tag)
            ind= word+' / '+ tag
            emiscount[ind]+= 1
        tags.append(tempt)
    
    #emisprob
    emisprob=defaultdict(float)
    for key,val in emiscount.items():
        temptag= key.split(' / ')[1]
        emisprob[key]= float(val)/float(tagcount[temptag])
        #print(temptag) 
    
    
    #first and last tags
    firstags=defaultdict(float)
    lastags=defaultdict(float)
    
    #transany, trasncount
    transanycount=Counter()
    transcount=Counter()
    n= len(data)
    v=len(tagsdistinct)
    for t in tags:
        firstags[t[0]]+=1
        lastags[t[-1]]+=1
        for x in range(len(t)-1):
            transanycount[t[x]] +=1
            transcount[t[x]+','+t[x+1]] +=1
    
    
    for t in tagsdistinct:
        firstags[t]= float(firstags[t]+1)/float(n + v)
        lastags[t]= float(lastags[t]+1)/float(n + v)
        
        
    #transprob
    transprob=defaultdict(float)
    v=len(tagsdistinct)
    for t1 in tagsdistinct:
        for t2 in tagsdistinct:
            newval=float(transcount[t1+','+t2] + 1)/float(transanycount[t1] + v)
            transprob[t1+','+t2]=newval
    
    with open('hmmmodel.txt','w+',encoding='utf8') as output:
        output.write("All tags available:"+"\n")
        for cl in tagsdistinct:
            output.write(str(cl) + " ")
        output.write("\n")
        output.write("Vocab: "+"\n")
        for v in vocab:
            output.write(str(v) + " ")
        output.write("\n")
        output.write("Emission Probabilities "+"\n")
        output.write(json.dumps(emisprob))
        output.write("\n")
        output.write("Transition Probabilities"+"\n")
        output.write(json.dumps(transprob))
        output.write("\n")
        output.write("First Transition Probabilities...a(0,s)"+"\n")
        output.write(json.dumps(firstags))
        output.write("\n")
        output.write("Last Transition Probabilities....a(s,qf)"+"\n")
        output.write(json.dumps(lastags))
        
        
