# -*- coding: utf-8 -*-
import requests
import csv
import re
import os
import urllib
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
def save_img(img_url,file_name,file_path='caixi\sucai'):#苏菜就是caixi/sucai   鲁菜就是caixi/lucai
    try:
        if not os.path.exists(file_path):
            print ('文件夹',file_path,'不存在，重新建立')
            #os.mkdir(file_path)
            os.makedirs(file_path)
        #获得图片后缀
        file_suffix = os.path.splitext(img_url)[1]
        #拼接图片名（包含路径）
        filename = '{}{}{}{}'.format(file_path,os.sep,file_name,file_suffix)
       #下载图片，并保存到文件夹中
        urllib.request.urlretrieve(img_url,filename=filename)
    except IOError as e:
        print ('文件操作失败',e)
    except Exception as e:
        print ('错误 ：',e)
def get_full_information(urls):
    count=0
    countLength=len(urls)
    for url in urls:
        content=requests.get(url).text
        soup= BeautifulSoup(content,'lxml')
        cai_name=soup.find('a',id='tongji_title')
        cai_img_url=re.findall('<img alt=".*?" src="(.*?)" />',content)[0]
        if cai_name!=None:
            cai_name=cai_name.get_text()
        save_img(cai_img_url,cai_name)
        count=count+1
        print ("%.2f"% (count/countLength))    
if __name__ == '__main__':
#    img_url = 'http://s1.st.meishij.net/r/127/79/6144877/a6144877_151766522396327.jpg'
#    save_img(img_url,'jianshu')
    url=['http://www.meishij.net/china-food/caixi/sucai/?&page={}'.format(str(i)) for i in range(1,2)]
    urls=get_link(url)
    get_full_information(urls)


