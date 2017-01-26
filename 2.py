from bs4 import BeautifulSoup
import requests
import re
import jieba
import pymysql
#import chardet
#import thulac
#import time
### output ###
# input（url）：新闻页面地址
# return：properties：新闻中关键字的字典以及词频，包括时间 time

def catchkeyword(url):
    properties = {}
    html = requests.get(url)
    html.encoding = 'utf-8'
    soup=BeautifulSoup(html.text,'html.parser')
    try:
        content=soup.select('.detailtext')
        for word in jieba.cut(content[0].text, cut_all=False):
            properties[word] = properties.get(word, 0) + 1
        time = str(soup.select('.tips')[0])
        #properties['time']=re.findall(time_rule,time)[0]
        return properties
    except Exception as err:
        return {}
def insert_data(data):
    for key in data:
       try:
           cursor.execute("SELECT * FROM KEY_count3 WHERE KEY_WORD ='%s'"%(key))
           db.commit()
           results = cursor.fetchall()
           if not results:
               cursor.execute("INSERT INTO KEY_count3(KEY_WORD,COUNT0) VALUES ('%s','%d')"%(key,data[key]))
               db.commit()
               results=()
           else:
               cursor.execute("UPDATE KEY_count3 SET COUNT0 = COUNT0 + '%d' WHERE KEY_WORD = '%s'"%(data[key],key))
               db.commit()
               results = ()
       except Exception as error3:
             print(error3)
time_rule = re.compile(r'\d{4}-\d{2}-\d{2}')
# 打开数据库连接
db = pymysql.connect(host='123.207.167.196', port=3306, user='python', passwd='############', db='python',charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
db.commit()
# 使用 execute() 方法执行 SQL，如果表存在则删除
#cursor.execute("DROP TABLE IF EXISTS python")
# 使用预处理语句创建表
sql = """CREATE TABLE KEY_count3(
         KEY_WORD CHAR(20) NOT NULL,
         COUNT0 INT )"""
#cursor.execute(sql)
#print(catchkeyword('http://news.xpu.edu.cn/info/1003/4037.htm'))
first=[1002,1003,1011,1012,1016,1017]#构造一级目录
secend = [i for i in range(4035,4038)]#购机二级目录
url='http://news.xpu.edu.cn/info/'+str(first[1])+'/'+str(secend[2])+'.htm'#构造网址
for  t in  secend:
    for i in first:
        url = 'http://news.xpu.edu.cn/info/' + str(i) + '/' + str(t) + '.htm'  # 构造网址
        result=catchkeyword(url)
        if  result:
            insert_data(result)
        else:
            pass


