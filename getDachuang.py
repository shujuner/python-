# -*- coding: utf-8 -*-
import requests
import re
import csv
import os,time
os.environ['NO_PROXY'] = 'stackoverflow.com'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'      
}
def get_data(url):
    content=requests.get(url).text
    scode=re.findall('"scode":"(.*?)",',content)
    sname=re.findall('"sname":"(.*?)",',content)
    basiceps=re.findall('"basiceps":(.*?),',content)
    cutbasiceps=re.findall('"cutbasiceps":(.*?),',content)
    totaloperatereve=re.findall('"totaloperatereve":(.*?),',content)
    ystz=re.findall('"ystz":(.*?),',content)
    parentnetprofit=re.findall('"parentnetprofit":(.*?),',content)
    sjltz=re.findall('"sjltz":(.*?),',content)
    sjlhz=re.findall('"sjlhz":(.*?),',content)
    roeweighted=re.findall('"roeweighted":(.*?),',content)
    bps=re.findall('"bps":(.*?),',content)
    mgjyxjje=re.findall('"mgjyxjje":(.*?),',content)
    xsmll=re.findall('"xsmll":(.*?),',content)
    publishname=re.findall('"publishname":"(.*?)",',content)
    for i in range(0,50):
        data=[]
        data.append(scode[i])
        data.append(sname[i])
        data.append(basiceps[i])
        data.append(cutbasiceps[i])
        data.append(totaloperatereve[i])
        data.append(ystz[i])
        data.append(parentnetprofit[i])
        data.append(sjltz[i])
        data.append(sjlhz[i])
        data.append(roeweighted[i])
        data.append(bps[i])
        data.append(mgjyxjje[i])
        data.append(xsmll[i])
        data.append(publishname[i])
        with open("dachuang/2017first.csv","a",newline='') as csvfile: 
            writer = csv.writer(csvfile)
            writer.writerow(data)
urls=[]
for i in range(0,69):
    urls.append('http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=YJBB20_YJBB&token=70f12f2f4f091e459a279469fe49eca5&st=latestnoticedate&sr=-1&p={}&ps=50&filter=(reportdate=^2017-3-31^)'.format(str(i)))
print (urls)
count=0
for url in urls:
    get_data(url)
    print ('%.2f'%(count/73))
    count+=1