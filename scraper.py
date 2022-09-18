import requests
from bs4 import BeautifulSoup
import urllib
import time

class corsidimoto:
    def __init__(self):
        pass

    def find_articlelist(self, url):
        self.topurl = url
        self.response = requests.get(self.topurl)
        self.soup = BeautifulSoup(self.response.content, "html.parser")
        self.rowlist = []
        self.rowlist = self.soup.find_all("div", attrs={"class": "main-post-loop"})
        self.alist = []
        for self.e in self.rowlist:
            self.articleurl = self.e.find("h2").find("a").get("href")
            if self.articleurl is not None:
                self.alist.append(self.articleurl)

        return self.alist

    def find_article(self, url):
        self.aurl = url
        self.response = requests.get(self.aurl)
        self.soup2 = BeautifulSoup(self.response.content, "html.parser")
    #find article
        self.a = self.soup2.find("div", attrs={"class": "blog-post-item"})
        if self.a is None:
            return None
    #get title
        self.title_text = self.a.find("h1").get_text(strip = True)
        if self.title_text is None:
            self.title_text = ''

        self.cont = self.a.find("div", attrs={"class": "content_text"})
        if self.cont is None:
            return None
        self.plist = self.cont.find_all("p")
        if self.plist is None:
            return None
        #translate title if it is not null
        self.contentlist = []
        if self.title_text != '':
            self.contentlist.append(self.title_text)
        #translate all paragraphs
        for self.para in self.plist:
            self.contentlist.append(self.para.get_text(strip = True))

        return self.contentlist

class motociclismo:
    def __init__(self):
        pass

    def find_articlelist(self, url):
        self.topurl = url
        self.response = requests.get(self.topurl)
        self.soup = BeautifulSoup(self.response.content, "html.parser")
        self.rowlist = []
        self.rowlist = self.soup.find_all("div", attrs={"class": "c-news-list__item"})
        
        self.alist = []
        for self.e in self.rowlist:
            self.articleurl = self.e.find("a", {"class": "c-news-list__titlelink"}).get("href")
            if self.articleurl is not None:
                print(self.articleurl)
                self.alist.append(self.articleurl)

        return self.alist

    def find_article(self, url):
        self.aurl = url
        self.response = requests.get(self.aurl)
        self.soup2 = BeautifulSoup(self.response.content, "html.parser")
    #find article
    
    #get title
        self.title = self.soup2.find("h1", attrs={"class": "c-mainarticle__title"})
        if self.title is not None:
            self.title_text = self.title.get_text(strip = True)
        else:
            self.title_text = ''

        self.cont = self.soup2.find("div", attrs={"class": "c-mainarticle__body"})
        if self.cont is None:
            return None
        self.plist = self.cont.find_all("p")
        if self.plist is None:
            return None
        #translate title if it is not null
        self.contentlist = []
        if self.title_text != '':
            self.contentlist.append(self.title_text)
        #translate all paragraphs
        for self.para in self.plist:
            self.contentlist.append(self.para.get_text(strip = True))

        return self.contentlist


class worldsbk:
    def __init__(self):
        pass
    
    def find_articlelist(self, url):
        self.topurl = url
        self.response = requests.get(self.topurl)
        self.soup = BeautifulSoup(self.response.content, "html.parser")
        self.templist = self.soup.find("div", attrs={"class": "row content-items-list"})
        self.alist = []
        self.rowlist = self.templist.find_all("a")
        for self.e in self.rowlist:
            if self.e.find("article", attrs={"class": "news-item"}) is not None:
                self.alist.append( urllib.parse.urljoin(self.topurl, self.e.get("href")))
        return self.alist

    def find_article(self, url):
        self.aurl = url
        self.response = requests.get(self.aurl)
        self.soup2 = BeautifulSoup(self.response.content, "html.parser")

#        print(self.response.content)
        self.head = self.soup2.find("article", attrs={"class": "news-item"})
        if self.head is not None:
            self.title_text = self.head.find("header").find("h2").get_text(strip = True)
        else:
            self.title_text = ''

        self.cont = self.soup2.find("div" , attrs={"class": "content"})
        if self.cont is None:
            return None
#        print (f"{self.aurl}, {self.cont}")
        self.plist = self.cont.find_all("p")
        if self.plist is None:
            return None
        #translate title if it is not null
        self.contentlist = []
        if self.title_text != '':
            self.contentlist.append(self.title_text)
        #translate all paragraphs
        for self.para in self.plist:
            self.contentlist.append(self.para.get_text(strip = True))

        return self.contentlist

class speedweek_motogp:
    def __init__(self):
        pass
    
    def find_articlelist(self, url):
        self.topurl = url
        self.response = requests.get(self.topurl)
        self.soup = BeautifulSoup(self.response.content, "html.parser")

        self.siteurl = "http://speedweek.com/"
        self.divlist = self.soup.find_all("div", {"id": "sw-masonry-content"})
        if self.divlist is None:
            print ("divlist is none")
            return None
#        else:
#            print (self.divlist)
        self.alist = []
        for self.e in self.divlist:
            self.elist = self.e.find_all("article", {"class": "tsr-news"})
            for self.e in self.elist:
                self.eurl = self.e.find("a", {"class": "stretched-link"})
#                print (f"e = {self.e} url = {self.eurl}")
                self.alist.append(urllib.parse.urljoin(self.siteurl, self.eurl.get("href")))

        return self.alist

    def find_article(self, url):
        self.aurl = url
        self.response = requests.get(self.aurl)
        self.soup2 = BeautifulSoup(self.response.content, "html.parser")

#        print(self.response.content)
        self.head = self.soup2.find("article", {"class": "sw-art"})
        if self.head is not None:
            self.title_text = self.head.find("h1").get_text(strip = True)
        else:
            self.title_text = ''

        self.cont = self.soup2.find("div" , {"id": "sw-art-text"})
        if self.cont is None:
            return None
#        print (f"{self.aurl}")
        self.plist = self.cont.find_all("p")
        if self.plist is None:
            return None
        #translate title if it is not null
        self.contentlist = []
        if self.title_text != '':
            self.contentlist.append(self.title_text)
        #translate all paragraphs
        for self.para in self.plist:
            self.contentlist.append(self.para.get_text(strip = True))

        return self.contentlist

        
