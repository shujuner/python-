# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 15:00:44 2018

@author: 15
"""
import requests
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool
import csv
count=0
#length=0
def getFirstLayerLink(baseUrl):
    firstLink=[]
    for i in range(0,250,25):
        url="%s%d"%(baseUrl,i)
        firstData = requests.get(url).text  
        needData = re.findall('<a href="(.*?)" class="">',firstData)
        for j in range(len(needData)):
            goodJudge=needData[j]+'comments?start=0&limit=20&sort=new_score&status=P&percent_type=h'
            normalJudge=needData[j]+'comments?start=0&limit=20&sort=new_score&status=P&percent_type=m'
            badJudge=needData[j]+'comments?start=0&limit=20&sort=new_score&status=P&percent_type=l'
            firstLink.append(goodJudge)
            firstLink.append(normalJudge)
            firstLink.append(badJudge)
    return firstLink 
def getData(url):
    #count=0
    #for url in urls:
    r = requests.get(url)
    content=r.text
    soup = BeautifulSoup(content,'lxml')
    i=0
    for item in soup.find_all('span',class_='comment-info'):
        data=[]
        movie_id=url.replace("https://movie.douban.com/subject/","").replace("/comments?start=0&limit=20&sort=new_score&status=P&percent_type=","").strip('hml')
        user_id=item.find('a',class_="").get('href').replace("https://www.douban.com/people/","").strip('/')
        rating5=item.find('span',class_="allstar50 rating")
        rating4=item.find('span',class_="allstar40 rating")
        rating3=item.find('span',class_="allstar30 rating")
        rating2=item.find('span',class_="allstar20 rating")
        rating1=item.find('span',class_="allstar10 rating")
        if rating5!=None:
            rating=5
        elif rating4!=None:
            rating=4
        elif rating3!=None:
            rating=3
        elif rating2!=None:
            rating=2
        elif rating1!=None:
            rating=1
        else:
            rating=0
        time=item.find('span',class_="comment-time").text.strip()
        data.append(user_id)
        data.append(movie_id)
        data.append(rating)
        data.append(time)
        print (data)
        with open("doubanTop10.txt","a",newline='') as csvfile: 
            writer = csv.writer(csvfile)
            print (data)
            writer.writerow(data)
        i=i+1
        if i>10:
            break
    global count
    count=count+1
    print ("%.2f"% (count/length))
if __name__=="__main__":
    urls=getFirstLayerLink('https://movie.douban.com/top250?start=')
    length=len(urls)
    print ('初始化完成')
    pool=Pool(processes=4)
    pool.map(getData,urls)
    print ('数据爬取完成')
    #url='https://movie.douban.com/subject/1292052/comments?start=0&limit=20&sort=new_score&status=P&percent_type=h'
    #urls=['https://movie.douban.com/subject/1292052/comments?start=0&limit=20&sort=new_score&status=P&percent_type=h','https://movie.douban.com/subject/1292052/comments?start=0&limit=20&sort=new_score&status=P&percent_type=m','https://movie.douban.com/subject/1292052/comments?start=0&limit=20&sort=new_score&status=P&percent_type=l']
    
        

    
    
    