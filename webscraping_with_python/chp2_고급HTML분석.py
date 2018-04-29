## class 와 id로 scraping하기

from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bsObj = BeautifulSoup(html, "html.parser")

nameList = bsObj.find_all("span", {"class": "green"})     #find_All(tagName, tagAttribute)
for name in nameList:
    print(name.get_text())


## 자식 자손 tag사용하기 : table태그의 자식 태그만 출력

from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "html.parser")

for child in bsObj.find("table", {"id" : "giftList"}).children:
    print(child)


## 형제 tag 사용하기 : 첫번째 객체를 제외한 나머지

from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "html.parser")

for sibling in bsObj.find("table", {"id" : "giftList"}).tr.next_siblings:
    print(sibling)


## BeautifulSoup + regex

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "html.parser")
images = bsObj.find_all("img", {"src":re.compile("\.\.\/img/gifts/img.*\.jpg")})
for image in images:
    print(image["src"])   # image 속성 - src에 접근하기


## lambda expression : find_all함수의 parameter로 함수 설정 가능

print(bsObj.find_all(lambda tag: len(tag.attrs)==2))