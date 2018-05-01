

## 데이터를 csv로 저장

import csv

csvFile = open("test.csv", 'w+')
try:
    writer = csv.writer(csvFile)
    writer.writerow(('number', 'number plus 2', 'number times 2'))
    for i in range(10):
        writer.writerow((i, i+2, i*2))

finally:
    csvFile.close()


## 데이터를 csv로 저장

import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://en.wikipedia.org/wiki/Comparison_of_text_editors")
bsObj = BeautifulSoup(html, "html.parser")

table = bsObj.find_all("table", {"class": "wikitable"})[0]
rows = table.find_all("tr")
csvFile = open("editors.csv", "wt")
writer = csv.writer(csvFile)

try:
    for row in rows:
        csvRow = []
        for cell in row.find_all(['td', 'th']):
            csvRow.append(cell.get_text().encode('utf-8'))
        writer.writerow(csvRow)
finally:
    csvFile.close()



## 데이터를 mySQL로 저장 : MySQLdb 활용
### https://mysqlclient.readthedocs.io/user_guide.html#connection-objects

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import MySQLdb

db = MySQLdb.connect(host='127.0.0.1', user='root',  passwd='trio034*', db='mysql', charset='utf8') #데이터를 utf-8형식으로 전송
c = db.cursor()
c.execute("USE scraping") #scraping 데이터베이스 사용 (pages라는 table이 생성되어 있음)

random.seed(datetime.datetime.now())

def store(title, content):
    c.execute(
        "INSERT INTO pages (title, content) VALUES (\"%s\", \"%s\")",
        (title, content)
    )
    c.connection.commit()

def getLink(articleUrl):  # /wiki로 시작하는 태그들을 추출

    html = urlopen("https://en.wikipedia.org" + articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")

    title = bsObj.find("h1").get_text()
    content = bsObj.find(id = "mw-content-text").find_all("p")[0].get_text()  # contents (text)
    store(title, content)

    return bsObj.find("div", {"id": "bodyContent"}).find_all("a",
                                                             href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLink("/wiki/Kevin_Bacon")

try:
    while len(links) > 0:
        newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
        print(newArticle)
        links = getLink(newArticle)  # 추출된 태그들 중 랜덤하게 하나를 선택, 앞선 작업을 반복
finally:
    c.close()
    db.close()

