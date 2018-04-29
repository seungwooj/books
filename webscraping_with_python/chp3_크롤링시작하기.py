
## wikipedia Kevin Bacon페이지 링크 가져오기 :

from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re
random.seed(datetime.datetime.now())

def getLink(articleUrl):    # /wiki로 시작하는 태그들을 추출


    html = urlopen("https://en.wikipedia.org" + articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    return bsObj.find("div", {"id" : "bodyContent"}).find_all("a",
                        href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLink("/wiki/Kevin_Bacon")
while len(links) > 0:
    newArticle = links[random.randint(0,len(links)-1)].attrs["href"]
    print(newArticle)
    links = getLink(newArticle)  # 추출된 태그들 중 랜덤하게 하나를 선택, 앞선 작업을 반복


## 전체사이트에서 특정 데이터를 출력

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set() #검색한 페이지들을 add할 page (set - 중복된 페이지는 제거) 생성

def getLinks(pageUrl):    # /wiki로 시작하는 태그들을 추출

    global pages   #page를 전역변수로 설정 (아래 함수에 지속적으로 적용되도록)

    html = urlopen("https://en.wikipedia.org" + pageUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    for link in bsObj.find_all("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:   #새페이지를 발견!
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)

# 전체 사이트에서 특정 데이터를 출력하기 : 페이지 제목, 첫문단, 편집페이지 링크 확인 + 이후 pages에 쌓기

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()
def getLinks(pageUrl):

    global pages
    html = urlopen("http://en.wikipedia.org" + pageUrl)
    bsObj = BeautifulSoup(html, "html.parser")

    try:  #try / except로 try에 해당되는 것들만 이후 크롤링 할 수 있도록 코딩
        print(bsObj.h1.get_text())    #h1 (title_
        print(bsObj.find(id = "mw-content-text").find_all("p")[0])  # contents (text)
        print(bsObj.find(id = "ca-edit").find("span").find("a").attrs["href"])   # edit button

    except AttributeError:
        print("This page is missing. No worries though!")  #없을 경우 에러 출력

    for link in bsObj.find_all("a", href=re.compile("^(/wiki/)")):

        #앞서 걸러진 try부분에 한하여 이후는 위와 동일 새 페이지 발견시 pages 에 넣기

        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print("-------------\n" + newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks("")

