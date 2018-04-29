

from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())


# 페이지에서 발견된 내부 링크를 list로 (internalLinks)

def getInternalLinks(bsObj, includeUrl):

    includeUrl = urlparse(includeUrl).scheme+"://"+urlparse(includeUrl).netloc
    internalLinks = []

    # /로 시작하는 링크를 모두 찾는다

    for link in bsObj.find_all("a", href=re.compile("^(/|.*" + includeUrl + ")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if (link.attrs['href'].startswith("/")):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks


# 페이지에서 발견된 외부 링크를 list로 (externalLinks)

def getExternalLinks(bsObj, excludeUrl):

    externalLinks = []

    # 현재 URL 을 포함하지 않으면서 http나 www로 시작하는 링크를 찾는다

    for link in bsObj.find_all("a", href = re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
               externalLinks.append(link.attrs['href'])
    return externalLinks

def getRandomExternalLink(startingPage):

    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html, "html.parser")
    externalLinks = getExternalLinks(bsObj, urlparse(startingPage).netloc)

    if len(externalLinks) == 0:
        domain = urlparse(startingPage).scheme+"://"+urlparse(startingPage).netloc
        internalLinks = getInternalLinks(bsObj, domain)
        return getRandomExternalLink(internalLinks[random.randint(0,len(internalLinks)-1)])

    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print("Random external link is:" + externalLink)
    followExternalOnly(externalLink)

followExternalOnly("http://oreilly.com")


# 사이트에서 찾은 외부 URL을 모두 리스트로 수집

allExtLinks = set()
allIntLinks = set()

def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    internalLinks = getInternalLinks(bsObj, splitAddress(domain)[0])
    externalLinks = getExternalLinks(bsObj, splitAddress(domin)[0])

    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)

    for link in internalLinks:
        if link == "/":
            link = domain
        elif link[0:2] == "//":
            link = "http:" + link
        elif link[0:1] == "/":
            link = domain + link

        if link not in allIntLinks:
            print("About to get link :" + link)
            allIntLinks.add(link)
            getAllExternalLinks(link)

domain = "http://oreilly.com"
getAllExternalLinks(domain)
