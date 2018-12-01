# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool
import csv
def getLink(urls):
    list=[]
    for url in urls:
        content=requests.get(url).text
        needData = re.findall('"url":"(.*?)"',content)
        for link in needData:
            link=link.replace("\/","/")
            list.append(link)
    return list
def dealUrl(needData):
    firstLink=[]
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
        with open("doubanByType.txt","a",newline='') as csvfile: 
            writer = csv.writer(csvfile)
            writer.writerow(data)
        if i>4:
            break   
if __name__=="__main__":
    url1=['https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start={}&limit=20'.format(str(i)) for i in range(0,200,20)]
    url2=['https://movie.douban.com/j/chart/top_list?type=24&interval_id=100%3A90&action=&start={}&limit=20'.format(str(i)) for i in range(0,200,20)]
    url3=['https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start={}&limit=20'.format(str(i)) for i in range(0,200,20)]
    urls1=getLink(url1)
    urls2=getLink(url2)
    urls3=getLink(url3)
    urls=dealUrl(urls1+urls2+urls3)
    print (len(urls))
    print ('初始化完成')
    print(urls[0],urls[1],urls[2])
    pool=Pool(processes=4)
    pool.map(getData,urls)