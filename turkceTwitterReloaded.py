# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 11:45:16 2017

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
userDict={}

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
    
def plotBars(xlabel,ylabel,wordValues,CommonWordList,worddDict,rDict):
    sent_series = pd.Series.from_array(wordValues) 


    plt.figure(figsize=(102, 15))
    ax = sent_series.plot(kind='bar')
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    rects = ax.patches
    labels = []
    i=0
#    label=""

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
            ax.text(rect.get_x() + rect.get_width()/2, height , label, ha='center', va='bottom')
            i=i+1

    
def checkPunctuation(letter):
    if letter=='.' or letter==',' or letter=='?' or letter=='!' or letter=='"' or letter==':'or letter==' 'or letter==';'or letter=='\n'or letter=='\t':
        return True
    else:
        return False

            
def cleanUpPunct(word):
    letterList=""
    for ii in range(len(word)):
        if not checkPunctuation(word[ii]):
            letterList=letterList+word[ii]
            
    return letterList            
            
            
def getReverseDict( wDict):
    reverseDict={}
    for word in wDict:
        wValue=wDict[word]
        if wValue not in reverseDict:
            reverseDict[wValue]=[word]
        else:
            reverseDict[wValue].append(word)
    return reverseDict
    
    
    
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

def addToUserDict(user,word,userDict):
    if user in userDict:
        wDict=userDict[user]
        wDict=incrementToDict(word,wDict)
        userDict[user]=wDict
    else:
        wDict={}
        wDict=incrementToDict(word,wDict)
        userDict[user]=wDict
    return userDict
        

def getUserDict(split_tl,userDict):
    for phrase in split_tl:
            topic,user,tweet=parseIntoThree(phrase)
            if not(user==""):
                for word in tweet:
                    word=word.lower()
                    word=cleanUpPunct(word)
                    if word not in stop and word not in stop2:
                        userDict=addToUserDict(user,word,userDict)
    return userDict

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

def getLists(split_tl):
    userList=[]
    subjectList=[]
    for phrase in split_tl:
            topic,user,tweet=parseIntoThree(phrase)    
            userList.append(user)
            subjectList.append(topic)
            
    return [userList,subjectList]

def getMaxWPerP(word,pDict):
    occurrance=0
    
    for dictionary in pDict:
        personListDict=pDict.values()
        for dictionary2 in personListDict:
            try:
                
                number=dictionary2[word]
            except:
                number=0
#            print number  
            if number>occurrance:
                occurrance=number
    
    return occurrance
    
def totalNoise2(wordDict,commonWordList,epsilon,pDict):
    import numpy as np
    import math
    newDict=wordDict.copy()
    epsilon=1.0*epsilon/len(commonWordList)
    for wList in commonWordList:
        
        for word in wList:
            
            delta=getMaxWPerP(word,pDict)
            noise=math.fabs(np.random.laplace(delta,1/epsilon))
#            factor=math.fabs(np.random.laplace(0,epsilon))
            #factor=math.fabs(delta*epsilon)

            print newDict[word]
            newDict[word]+=int(noise)
#            print newDict[word]
            print noise
    return newDict


#Main Program

############################################
[userTweet2,topicTweet2,userTopic2,topicWord2]=returnDicts(split_tl,userTweet1,topicTweet1,userTopic1,topicWord1)
[userTweetEx,topicTweetEx,userTopicEx,topicWordEx]=returnDictsExUser(split_tl,userTweet1,topicTweet1,userTopic1,topicWord1,'siirvekadin')



#Normal
topic='Spor'
dict1=getTopicDict(topicWord2,topic)

maxNum=30
[CommonWordList1,wordValues1]=getCommonWords(maxNum,dict1)
rDict1=getReverseDict(dict1)
#print getCommonWordCount(dict1)

plotBars("Words","Number of Occurances",wordValues1,CommonWordList1,dict1,rDict1)

epsilon=1.0

userDict=getUserDict(split_tl,userDict)
newDictOrNoised=totalNoise2(dict1,CommonWordList1,epsilon,userDict)



