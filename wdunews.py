import requests
import datetime
from bs4 import BeautifulSoup
from lxml import etree
from urllib import parse
import MySQLdb
#from sqlcon.models import Wdu

conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="testsql",charset="utf8")
cur=conn.cursor()
cur.execute("delete from final_result")

def getcontent():
    for i in range(1640,1648):
        link="http://news.wzu.edu.cn/wdxw/"+str(i)+".htm"

        r=requests.get(link)
        r.encoding="UTF-8"

        tree=etree.HTML(r.text)
        time1=tree.xpath("//div[@class='ym']/text()")
        time2=tree.xpath("//div[@class='d']/text()")
        time=[]
        for i in range(len(time1)):
            time.append(time1[i]+"-"+time2[i])

       
        href=tree.xpath("//div[@class='tit']/a/@href")
        href=[parse.urljoin(link,i) for i in href]

        title=tree.xpath("//div[@class='tit']/a/@title")
        content=tree.xpath("//div[@class='jj']/text()")

        for i in range(len(title)-1):
            Title=title[i]
            Href=href[i]
            Time=time[i]
            Content=content[i]
            #record=Wdu(title=Title,time=Time,href=Href,content=Content)
            #record.save()
            cur.execute("insert into final_result(title,time,href,content) values(\"%s\",\"%s\",\"%s\",\"%s\")"%(Title,Time,Href,Content))
getcontent()
conn.commit()
conn.close()
