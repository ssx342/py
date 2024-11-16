import requests

import urllib.parse

import time

import chardet
import pymysql
import requests
from lxml import etree

import DBhelper

def load_page(url):

    headers = {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",

        "Cookie": "ddscreen=2; dest_area=country_id%3D9000%26province_id%3D111%26city_id%20%3D0%26district_id%3D0%26town_id%3D0; __permanent_id=20240613173907034342720395805643511; __visit_id=20240613173907056132662234101569443; __out_refer=1718271547%7C!%7Cwww.so.com%7C!%7C; __rpm=%7Cmix_317715.4162651%2Cseckill.7.1718273822809; __trace_id=20240613182152943294024180746500433"}
    try:
        response=requests.get(url,headers=headers,timeout=2)
        response.encoding=chardet.detect(response.content)['encoding']
        html=response.text
        return  html
    except:
        print("获取数据失败"+url)





def parse_page(html):
    conn=pymysql.Connect(host='127.0.0.1',port=3306,user='root',password='123456',database='dddb')
    cursor=conn.cursor()
    root=etree.HTML(html)
    for elem in root.xpath('//*[@id="menu_list"]'):
        root2=etree.HTML(etree.tostring(elem,pretty_print=True))
        for index in root2.xpath('//*[@id="menulist_content"]'):
            root3=etree.HTML(etree.tostring(index,pretty_print=True))
            title=root3.xpath('//a/text()')
            print(title)
            links=root3.xpath('//a//@href')
            print(links)
            items=[]

            for i in range(0,len(links)):
                if links[i].find(' http://category.dangdang.com')!=1:
                    if links[i].find("http")==-1:
                        links[i]='http:'+links[i]
                    sql2="SELECT catName FROM catinfo WHERE catURL='%s'"
                    sql3=sql2%(links[i])

                    rowcount=cursor.execute(sql3)
                    if rowcount==0:
                        sql4="INSERT INTO catinfo(catName,catURL,errorTimes)VALUES(%s,%s,%s)"
                        name=title[i]
                        cursor.execute(sql4,(name,links[i],0))
                        conn.commit()






if __name__=="__main__":

   url='https://www.dangdang.com/'
   html = load_page(url)
   parse_page(html)
