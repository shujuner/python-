# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:29:46 2018

@author: 15
"""
import requests
import csv
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'      
}
def get_link(urls):
    links=[]
    for url in urls:
        r = requests.get(url,headers)
        content=r.text
        soup = BeautifulSoup(content,'lxml')
        for item in soup.find_all('div',class_='listtyle1'):
            link=item.find('a').get('href')
            links.append(link)
    return links
def get_18start_information(urls):
    count=0
    countLength=len(urls)
    for url in urls:
        data=[]
        content=requests.get(url).text
        soup= BeautifulSoup(content,'lxml')
        cai_name=soup.find('a',id='tongji_title')
        if cai_name!=None:
            cai_name=cai_name.get_text()
        cai_gy=re.findall('工艺：</strong><span >(.*?)</span>',content)
        if len(cai_gy)!=0:
            cai_gy=cai_gy[0]
        else:
            cai_gy=None
        cai_nd=soup.find('a',id='tongji_nd')
        if cai_nd!=None:
            cai_nd=cai_nd.get_text()
        cai_kw=soup.find('a',id='tongji_kw')
        if cai_kw!=None:
            cai_kw=cai_kw.get_text()
        cai_prsj=soup.find('a',id='tongji_prsj')
        if cai_prsj!=None:
            cai_prsj=cai_prsj.get_text()
        cai_gx=re.findall('<strong >菜系及功效：</strong>(.*?)<strong >',content)
        if len(cai_gx)!=0:
            cai_gx=cai_gx[0]
        else:
            cai_gx=None
        zhuliao=re.findall('·配　　料:                      <P>(.*?)',content)
        if len(zhuliao)!=0:
            zhuliao=soup.select('.edit.edit_class_0.edit_class_2 > ')
        else:
            zhuliao=None
        fuliao=re.findall('辅料：</strong>(.*?)<strong>',content)
        tiaoliao=re.findall('调料：</strong>(.*?)<p align="center" >',content)
        if len(fuliao)!=0:
            fuliao=fuliao[0]
        else:
            fuliao=None
        if len(tiaoliao)!=0:
            tiaoliao=tiaoliao[0]
        else:
            tiaoliao=None
        data.append(cai_name)
        data.append(cai_gy)
        data.append(cai_nd)
        data.append(cai_kw)
        data.append(cai_gx)
        data.append(cai_prsj)
        data.append(zhuliao)
        with open("lucai.csv","a",newline='') as csvfile: 
                writer = csv.writer(csvfile)
                writer.writerow(data)
        count=count+1
        print ("%.2f"% (count/countLength))
        
def get_full_information(urls):
    count=0
    countLength=len(urls)
    for url in urls:
        data=[]
        content=requests.get(url).text
        stepNum=re.findall('"step":"(.*?)"',content)
        if stepNum!=None:
            stepNum=stepNum[0]
        soup= BeautifulSoup(content,'lxml')
        cai_name=soup.find('a',id='tongji_title')
        if cai_name!=None:
            cai_name=cai_name.get_text()
        cai_gy=soup.find('a',id='tongji_gy')
        if cai_gy!=None:
            cai_gy=cai_gy.get_text()
        cai_nd=soup.find('a',id='tongji_nd')
        if cai_nd!=None:
            cai_nd=cai_nd.get_text()
        cai_kw=soup.find('a',id='tongji_kw')
        if cai_kw!=None:
            cai_kw=cai_kw.get_text()
        cai_prsj=soup.find('a',id='tongji_prsj')
        if cai_prsj!=None:
            cai_prsj=cai_prsj.get_text()
        cai_gx=soup.find('a',id='tongji_gx_0')
        if cai_gx!=None:
            cai_gx=cai_gx.get_text()
        zhuliao=soup.select('.yl.zl.clearfix > ul > li > div > h4 > a')
        zhuliao_string="/".join(str(s.text) for s in zhuliao if s is not None)
        fuliao=soup.select('.yl.fuliao.clearfix > ul > li > h4 > a')
        allData=soup.select('.yl.fuliao.clearfix')
        length=len(allData)
        fuliao_string=""
        tiaoliao_string=""
        if length==2:
            fuliao=allData[0]
            tiaoliao=allData[1]
            fuliao_temp=fuliao.select('ul > li > h4 > a')
            fuliao_string="/".join(str(s.text) for s in fuliao_temp if s is not None)
            tiaoliao_temp=tiaoliao.select('ul > li > h4 > a')
            tiaoliao_string="/".join(str(s.text) for s in tiaoliao_temp if s is not None)
        elif length==1:
            judge=soup.select('.yl.fuliao.clearfix > h3 > a')[0].text.strip()
            if judge=='辅料':
                fuliao=allData[0]
                fuliao_temp=fuliao.select('ul > li > h4 > a')
                fuliao_string="/".join(str(s.text) for s in fuliao_temp if s is not None)
                tiaoliao_string=""
            else:
                tiaoliao=allData[0]
                tiaoliao_temp=tiaoliao.select('ul > li > h4 > a')
                tiaoliao_string="/".join(str(s.text) for s in tiaoliao_temp if s is not None)
                fuliao_string=""
        data.append(cai_name)
        data.append(cai_gy)
        data.append(cai_nd)
        data.append(cai_kw)
        data.append(cai_gx)
        data.append(cai_prsj)
        data.append(zhuliao_string)
        data.append(fuliao_string)
        data.append(tiaoliao_string)
        data.append(stepNum)
        with open("testSucai.csv","a",newline='') as csvfile: 
                writer = csv.writer(csvfile)
                writer.writerow(data)
        count=count+1
        print ("%.2f"% (count/countLength))    

def multi_get_full_information(url):
    data=[]
    content=requests.get(url).text
    stepNum=re.findall('"step":"(.*?)"',content)
    if stepNum!=None:
        stepNum=stepNum[0]
    soup= BeautifulSoup(content,'lxml')
    cai_name=soup.find('a',id='tongji_title')
    if cai_name!=None:
        cai_name=cai_name.get_text()
    cai_gy=soup.find('a',id='tongji_gy')
    if cai_gy!=None:
        cai_gy=cai_gy.get_text()
    cai_nd=soup.find('a',id='tongji_nd')
    if cai_nd!=None:
        cai_nd=cai_nd.get_text()
    cai_kw=soup.find('a',id='tongji_kw')
    if cai_kw!=None:
        cai_kw=cai_kw.get_text()
    cai_prsj=soup.find('a',id='tongji_prsj')
    if cai_prsj!=None:
        cai_prsj=cai_prsj.get_text()
    cai_gx=soup.find('a',id='tongji_gx_0')
    if cai_gx!=None:
        cai_gx=cai_gx.get_text()
    zhuliao=soup.select('.yl.zl.clearfix > ul > li > div > h4 > a')
    zhuliao_string="/".join(str(s.text) for s in zhuliao if s is not None)
    fuliao=soup.select('.yl.fuliao.clearfix > ul > li > h4 > a')
    allData=soup.select('.yl.fuliao.clearfix')
    length=len(allData)
    fuliao_string=""
    tiaoliao_string=""
    if length==2:
        fuliao=allData[0]
        tiaoliao=allData[1]
        fuliao_temp=fuliao.select('ul > li > h4 > a')
        fuliao_string="/".join(str(s.text) for s in fuliao_temp if s is not None)
        tiaoliao_temp=tiaoliao.select('ul > li > h4 > a')
        tiaoliao_string="/".join(str(s.text) for s in tiaoliao_temp if s is not None)
    elif length==1:
        judge=soup.select('.yl.fuliao.clearfix > h3 > a')[0].text.strip()
        if judge=='辅料':
            fuliao=allData[0]
            fuliao_temp=fuliao.select('ul > li > h4 > a')
            fuliao_string="/".join(str(s.text) for s in fuliao_temp if s is not None)
            tiaoliao_string=""
        else:
            tiaoliao=allData[0]
            tiaoliao_temp=tiaoliao.select('ul > li > h4 > a')
            tiaoliao_string="/".join(str(s.text) for s in tiaoliao_temp if s is not None)
            fuliao_string=""
    data.append(cai_name)
    data.append(cai_gy)
    data.append(cai_nd)
    data.append(cai_kw)
    data.append(cai_gx)
    data.append(cai_prsj)
    data.append(zhuliao_string)
    data.append(fuliao_string)
    data.append(tiaoliao_string)
    data.append(stepNum)
    with open("fullSucai.csv","a",newline='') as csvfile: 
            writer = csv.writer(csvfile)
            writer.writerow(data)        
if __name__=="__main__":
    print ('start')
    url=['http://www.meishij.net/china-food/caixi/sucai/?&page={}'.format(str(i)) for i in range(1,57)]
    urls=get_link(url)
    print ('初始化完成')
    #get_full_information(urls)
    pool=Pool(processes=4)
    pool.map(multi_get_full_information,urls)
    print ('finish')
