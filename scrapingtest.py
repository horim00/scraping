import argparse
import requests
from bs4 import BeautifulSoup
import urllib
import time
import clipboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedCondition

import deepl
import scraper

class WebScraper:
    def __init__(self, scraper, driver, topurl, outftrunk, outfext,  histftrunk, histfext,  allnews):
        self.scraper = scraper
        self.driver = driver    #deepL driver
        self.topurl = topurl    #ual to start
        self.outftrunk= outftrunk       # output file name trunk (ex. "speedweek")
        self.outfext = outfext # output file extention (ex. ".txt")
        self.histftrunk = histftrunk      # history filename trunk  (ex. "speedweek-hist")
        self.histfext = histfext #history filename extention (ex. ".txt" )
        self.histset = set()    # history file name set
        self.allnews = allnews #  if true ignore history file and read all news
        self.fmt = "%Y%m%d%H%M%S"
        self.t = time.localtime()
        self.datestr = time.strftime(self.fmt, self.t)
        self.outf  = self.outftrunk + self.datestr + self.outfext
        self.histf = self.histftrunk + self.histfext
        
        #  Open history file and open selenium driver for DeepL.com
    def open(self):
        print(f"outfile   {self.outf}")
        self.outputfile = open(self.outf, "w", encoding='utf-8')
        try:
            with open(self.histf, "r", encoding="utf-8") as self.historyfile:
                self.lines = self.historyfile.readlines()
                for self.l in self.lines:
                    self.histset.add(self.l.strip())
        except FileNotFoundError:
            pass
        self.driver.open()

# This function  get article  list  from a url , translate each  new article  or all articles  and write translated text to output file
    def translate(self):
        self.alist = self.scraper.find_articlelist(self.topurl) # list of  articles to  be translated
        self.translate_check = set()   # set of  translated url s
        self.historyfile = open(self.histf, "w",  encoding="utf-8")
        for self.aurl in self.alist:
            #check if already translated
            if (self.aurl in self.translate_check):
                continue
            else:
                self.translate_check.add(self.aurl)
            print(f"{self.aurl}", file=self.historyfile)
            self.driver.refresh()
            
            # check if already seen
            if (self.is_seen(self.aurl)):
                continue
            # get paragraph text array as Python list
            self.contentlist = self.scraper.find_article(self.aurl)
            #translate
            if self.contentlist is None:
                continue
# output URL
            print(f"URL:  {self.aurl}", file=self.outputfile)
            for self.para in self.contentlist:
                self.translated = self.driver.translate(self.para)
                if self.translated is not None:
                    print(f"{self.translated}\r\n", file=self.outputfile)
            print("========", file=self.outputfile)

# This function close  history file, output file and selenium driver
    def close(self):
        self.historyfile.close()
        self.driver.close()
        self.outputfile.close()

# returns true  if  
#aurl:  a URL to be tested if included in the history file
# return  false is aurl is not in the history set
    def is_seen(self, aurl):
        if self.allnews:
            return False

        if (aurl in self.histset):
            print (f"{aurl} is seen.")
        return (aurl in self.histset)

#

parser = argparse.ArgumentParser(description='scrape websites')
parser.add_argument('-all', action='store_true', help='translate all news')
args = parser.parse_args()
deepldriver = deepl.Deepl()

websitelist = set()

speedweek_motogp_scraper = WebScraper(scraper.speedweek_motogp(), deepldriver, "https://www.speedweek.com/",
        "speedweek", ".txt", "speedweek-hist" , ".txt", args.all)
websitelist.add(speedweek_motogp_scraper)

#speedweek_motogp_scraper.open()
#speedweek_motogp_scraper.translate()
#speedweek_motogp_scraper.close()

corsidimoto_scraper = WebScraper(scraper.corsidimoto(), deepldriver, "https://www.corsedimoto.com/motomondiale/motogp/", 
        "corsedimoto-motogp", ".txt", "corsedimoto-motogp-hist", ".txt", args.all)
websitelist.add(corsidimoto_scraper)

#corsidimoto_scraper.open()
#corsidimoto_scraper.translate()
#corsidimoto_scraper.close()

motociclismo_motogp_scraper = WebScraper(scraper.motociclismo(), deepldriver, "https://www.motociclismo.es/mundial-motogp",
        "motociclismo-motogp", ".txt","moociclismo-motogp-txt", ".txt", args.all)
websitelist.add(motociclismo_motogp_scraper)
#motociclismo_motogp_scraper.open()
#motociclismo_motogp_scraper.translate()
#motociclismo_motogp_scraper.close()

motociclismo_deporte_scraper = WebScraper(scraper.motociclismo(), deepldriver, "https://www.motociclismo.es/deporte",
        "motociclismo-deporte", ".txt","moociclismo-deporte-hist", ".txt", args.all)
websitelist.add(motociclismo_deporte_scraper)
#motociclismo_deporte_scraper.open()
#motociclismo_deporte_scraper.translate()
#motociclismo_deporte_scraper.close()

worldsbk_scraper = WebScraper(scraper.worldsbk(), deepldriver, "https://www.worldsbk.com/", 
        "worldsbk", ".txt", "worldsbk-hist", ".txt", args.all)
websitelist.add(worldsbk_scraper)
#worldsbk_scraper.open()
#worldsbk_scraper.translate()
#worldsbk_scraper.close()

for website in websitelist:
    website.open()
    website.translate()
    website.close()
