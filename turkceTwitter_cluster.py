# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 11:45:16 2017

@author: Erman
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

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
personTopicDict={}

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


def addToPersonTopicDict(author,subject,personTopicDict):
    if author in personTopicDict:
        incrementToDict(subject,personTopicDict[author])
    else:
        dummy={}
        personTopicDict[author]=dummy
        incrementToDict(subject,personTopicDict[author])
        
    return personTopicDict
    
def formPersonTopicDict(split_tl,personTopicDict):
        for phrase in split_tl:
            topic,user,tweet=parseIntoThree(phrase)  
            personTopicDict=addToPersonTopicDict(user,topic,personTopicDict)
            
        return personTopicDict
        
def getFeaturesMatrix(subjectList,personList,personTopicDict):
    
    subjectLength=len(subjectList)
    personLength=len(personList)
    
    
    
    X=np.zeros([personLength,subjectLength])
    
    for ii in range(personLength):
        for jj in range(subjectLength):
            subject=subjectList[jj]
            author=personList[ii]
#            print subject,author
             
            try:
                X[ii][jj]=X[ii][jj]+1.0*personTopicDict[author][subject]

            except:
                continue
    return X  
    
def checkLength(Row,cutOff):
    sum=0.0
    for item in Row:
        sum+=item*item
    if math.sqrt(sum)>=cutOff:
        return True
    else:
        return False
        
def normalizeRow(Row):
    sum=0.0
    for item in Row:
        sum+=item*item
    normalized=math.sqrt(sum)
#    print Row,normalized
    for ii in range(len(Row)):
        Row[ii]=Row[ii]/normalized
#    print Row,normalized
    return Row

def redefineMatrix(X,cutOff):
    
    
    Xp=np.zeros([1,len(X[1,:])])
    
    for ii in range(len(X[:,1])):
        if checkLength(X[ii,:],cutOff):
            Xp=np.vstack((Xp, X[ii,:]))
    Xp=np.delete(Xp, 0, 0)  
    for ii in range(len(Xp[:,1])):    
        Xp[ii,:]=normalizeRow(Xp[ii,:])

    return Xp
    
def getSquareDifference(row1,row2):
    error=0.0
    for ii in range(len(row1)):
        error+= (row1[ii]-row2[ii])**2
    return error

def calculateError(labels,centers,fMatrix):
    error=0.0
    for ii in range(len(labels)):
        label=labels[ii]
        center=centers[label]
        location=fMatrix[ii,:]
        error+=getSquareDifference(center,location)
    return error
    
def optimizeClusterN(clusterNStart,ClusterNEnd,fMatrix):  
    from sklearn.cluster import KMeans
    delta=0.07
    error=100000.0
    clNumber=0
    labelsFinal=[]
    centersFinal=[]
    for clusterNumber in range(clusterNStart,ClusterNEnd):
        kmeans = KMeans(n_clusters=clusterNumber, random_state=0).fit(fMatrix)
        labels=kmeans.labels_
        centers=kmeans.cluster_centers_
        errorFound=calculateError(labels,centers,fMatrix)
#        print errorFound
        if errorFound<error:
            if math.fabs(error-errorFound)/error<delta:
                error=errorFound
                labelsFinal=labels
                centersFinal=centers
                clNumber=clusterNumber
                break
            else:
                error=errorFound
                labelsFinal=labels
                centersFinal=centers
                clNumber=clusterNumber
         
        
            
    return labelsFinal,centersFinal,clNumber
    
    
def getTagsOfCenters(centers):
       midTags=["Kultur Adami","Muallim","Acentaci","Dizici","Emlakci"]
       highTags=["Sanatci","Mudur","Kaptan Pilot","Ev Hanimi","Agaoglu"]
       
       cutOff1=0.25
       cutOff2=0.75
       tagsList=[]
       for ii in range(len(centers[:,1])):
           str=""
           for jj in range(len(centers[1,:])):
               if centers[ii,jj]>cutOff1:
                   if centers[ii,jj]>cutOff2:
                       str+=" "+highTags[jj]
                   else:
                       str+=" "+midTags[jj]
    
           if str=="":
                str="Featureless"
           tagsList.append(str)
       return tagsList

       
def tagUsers(labels,tagsList):
    userTags=[]
    for ii in range(len(labels)):
        userTags.append(tagsList[labels[ii]])
    
    return userTags    
    
    
############################################
#Cluster
cutOff=10.0
personTopicDict= formPersonTopicDict(split_tl,personTopicDict)   
[userList,subjectList]=getLists(split_tl)
subjectList=["Kültür-Sanat","Eğitim","Havayollari",'Tv Dizileri','Emlak/insaat']
X=getFeaturesMatrix(subjectList,userList,personTopicDict)
Xredefined=redefineMatrix(X,cutOff)

clusterBottom=2
clusterTop=50
[labelsFinal,centersFinal,clusterNumber]=optimizeClusterN(clusterBottom,clusterTop,Xredefined)


tagsList=getTagsOfCenters(centersFinal)
userTags=tagUsers(labelsFinal,tagsList)