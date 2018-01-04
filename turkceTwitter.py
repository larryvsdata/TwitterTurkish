# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 08:38:17 2016

@author: Erman
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
stop = set(stopwords.words('turkish')) 
stop2=['nin','',' ','  ','   ','dan',"i̇stanbul","i̇ste","i̇yi","i̇zmir","i̇l"]

with open('tweetsWithCategoriesTest.txt','r') as infile:
    text_in2=infile.read()
    
split_tl=text_in2.split("\t")

def parseIntoThree(phrase):
    phrase=phrase.split("\n")
    
    try:
        part2=phrase[1]
        topic=phrase[0]
        part2=part2.split()
        user=part2[0]
        tweet=part2[1::]
        
    except:
        topic=""
        user=""
        tweet=""
        
    return [topic,user,tweet]


############################
#Add into dictionaries

userTweet1={}
topicTweet1={}
userTopic1={}       
topicWord1={}

def addToDict(key,value,Dictionary):
    if key in Dictionary:
        Dictionary[key].append(value)
    else:
        Dictionary[key]=[value]

    return Dictionary
    
def incrementToDict(key,Dictionary):
    if key in Dictionary:
        Dictionary[key]+=1
    else:
        Dictionary[key]=1

    return Dictionary
    
def embedUserTopic(user,topic,Dictionary):
    
    if user in Dictionary:
        incrementToDict(topic,Dictionary[user])
    else:
        dummy={}
        dummy[topic]=1
        Dictionary[user]=dummy
    return Dictionary

def embedTopicWord(topic, word,Dictionary):
    if topic in Dictionary:
        incrementToDict(word,Dictionary[topic])
    else:
        dummy={}
        dummy[word]=1
        Dictionary[topic]=dummy
    return Dictionary
    
def getReverseDict( wDict):
    reverseDict={}
    for word in wDict:
        wValue=wDict[word]
        if wValue not in reverseDict:
            reverseDict[wValue]=[word]
        else:
            reverseDict[wValue].append(word)
    return reverseDict
    

def plotBars(xlabel,ylabel,wordValues,CommonWordList,worddDict,rDict):
    sent_series = pd.Series.from_array(wordValues) 


    plt.figure(figsize=(102, 15))
    ax = sent_series.plot(kind='bar')
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    rects = ax.patches
    labels = []
    i=0


    for rect in rects:
            height=wordValues[i]
            try:
                words=rDict[height]
                for word in words:
                    if word not in labels:
                        labels.append(word)
                        label=word
                        break
                
            except:
                print ""
            try:    
                ax.text(rect.get_x() + rect.get_width()/2, height , label, ha='center', va='bottom')
            except:
                print label
                
            i=i+1
            

    
def getCommonWords(maxNum,worddDict):    
    wordValues=worddDict.values()
    
    
    wordValues.sort(reverse=True)
    wordValues=wordValues[0:maxNum]
    
    RevDict=getReverseDict( worddDict)
    CommonWordList=[]
    
    for ii in range(maxNum):
        word=RevDict[wordValues[ii]]
        if word not in CommonWordList:
            CommonWordList.append( RevDict[wordValues[ii]])    
            
    return [CommonWordList,wordValues]

def getCommonWordCount(wordDict): 
    wordValues=wordDict.values()
        
    wordValues.sort(reverse=True)
    
    return wordValues[0]
    
    
    


def returnDicts(split_tl,userTweet,topicTweet,userTopic,topicWord):
    for phrase in split_tl:
            topic,user,tweet=parseIntoThree(phrase)
#            print topic,user,tweet
            if not(user==""):
                userTweet=addToDict(user,tweet,userTweet)
                topicTweet=addToDict(topic,tweet,topicTweet)
                userTopic=embedUserTopic(user,topic,userTopic)
#                tweet=tweet.split()
                for word in tweet:
                    if word not in stop and word not in stop2:
                        topicWord=embedTopicWord(topic, word,topicWord)
#                    else:
#                        topicWord=embedTopicWord(topic, 'stop',topicWord)
    return [userTweet,topicTweet,userTopic,topicWord]


def returnDictsExUser(split_tl,userTweet,topicTweet,userTopic,topicWord,userEx):
    for phrase in split_tl:
            topic,user,tweet=parseIntoThree(phrase)

            if not(user=="") and not(user==userEx):
                userTweet=addToDict(user,tweet,userTweet)
                topicTweet=addToDict(topic,tweet,topicTweet)
                userTopic=embedUserTopic(user,topic,userTopic)

                for word in tweet:
                    if word not in stop and word not in stop2:
                        topicWord=embedTopicWord(topic,word,topicWord)
            
    return [userTweet,topicTweet,userTopic,topicWord]


def getTopicDict(topicWord,topic):
    return topicWord[topic]


#Main Program

############################################

[userTweet2,topicTweet2,userTopic2,topicWord2]=returnDicts(split_tl,userTweet1,topicTweet1,userTopic1,topicWord1)
[userTweetEx,topicTweetEx,userTopicEx,topicWordEx]=returnDictsExUser(split_tl,userTweet1,topicTweet1,userTopic1,topicWord1,'siirvekadin')



#Normal
topic='Spor'
dict1=getTopicDict(topicWord2,topic)

maxNum=70
[CommonWordList1,wordValues1]=getCommonWords(maxNum,dict1)
rDict1=getReverseDict(dict1)
#print getCommonWordCount(dict1)

plotBars("Words","Number of Occurances",wordValues1,CommonWordList1,dict1,rDict1)


#After Ejection


topic='Spor'
dict2=getTopicDict(topicWordEx,topic)
rDict2=getReverseDict(dict2)

#print getCommonWordCount(dict2)

maxNum=50
[CommonWordList2,wordValues2]=getCommonWords(maxNum,dict2)

plotBars("Words","Number of Occurances",wordValues2,CommonWordList2,dict2,rDict2)


