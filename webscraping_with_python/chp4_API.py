

# get : 웹서버에 정보를 요청
# post : 웹서버에 정보를 보냄 -> 저장 요청 (ex) log-in : id & password)
# put : 웹서버의 정보를 업데이트 (ex> 사용자 이메일 주소를 업데이트, 변경)
# delete : 웹서버의 정보를 삭제





## wikipedia에서 사용자 url정보 가져오기

from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re
import json

random.seed(datetime.datetime.now())



def getLinks(articleUrl): # 페이지에 연결된 모든 계정내역을 가져온다

    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    return bsObj.find("div", {"id":"bodyContent"}).find_all("a",
                                                            href=re.compile("^(/wiki/)((?!:).)*$"))


def getHistoryIPs(pageUrl): #

    #개정 내역 페이지 URL의 형식
    #http://en.wikipedia.org/w/index.php?title=Title_in_URL&action=history

    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = "http://en.wikipedia.org/w/index.php?title="
    historyUrl += pageUrl + "&action=history"
    print("history url is :" + historyUrl)

    html = urlopen(historyUrl)
    bsObj = BeautifulSoup(html, "html.parser")

    ipAddresses = bsObj.find_all("a", {"class" : "mw-anonuserlink"}) #mw-anonuserlink : 익명의 사용자의 주소 에 대한 클래스
    addressList = set()
    for ipAddress in ipAddresses:
        addressList.add(ipAddress.get_text())

    return addressList


links = getLinks("/wiki/Python_(programming_language)")



## 코드 합칠 때 while문 주석처리 뒤의 함수 실행 X
# while (len(links) > 0):
#     for link in links:
#         print("-------------------")
#         historyIPs = getHistoryIPs(link.attrs["href"])
#         for historyIP in historyIPs:
#             print(historyIP)
#
#     newLink = links[random.randint(0, len(links)-1)].attrs["href"]
#     links = getLinks(newLink)

## freegeoip.net에서 IP주소의 country_code 가져오기

def getCountry(ipAddress):
    try:

        response = urlopen("http://freegeoip.net/json/"+ipAddress).read().decode('utf-8')

    except HTTPError:

        return None

    responseJson = json.loads(response)
    return responseJson.get("country_code")


links = getLinks("/wiki/Python_(programming_language)")


while (len(links) > 0):
    for link in links:
        print("---------------")
        historyIPs = getHistoryIPs(link.attrs["href"])
        for historyIP in historyIPs:
            country = getCountry(historyIP)
            if country is not None:
                print(historyIP+" is from "+country)

    newLink = links[random.randint(0, len(links)-1)].attrs["href"]
    links = getLinks(newLink)