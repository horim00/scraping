import urllib
import time
import clipboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedCondition
from selenium.webdriver.chrome.options import Options

class Deepl:

    def __init__(self):
        self.threshtime =  3 * 60
        self.lowthresh = 10
        self.deeplurl = "https://www.deepl.com/ja/translator"
        self.input_css = '.lmt__textarea.lmt__source_textarea.lmt__textarea_base_style'
        self.output_css = '.lmt__textarea.lmt__target_textarea.lmt__textarea_base_style'    
        self.maxlength = 4000
        self.chrome_options = Options()
#        self.chrome_options.add_argument("--headless")


    def open(self):
        self.driver = webdriver.Chrome(options = self.chrome_options)
        self.driver.get(self.deeplurl)
        self.starttime = time.time()

        self.input_area = self.driver.find_element(by=By.CSS_SELECTOR, value=self.input_css)
        self.output_area = self.driver.find_element(by=By.CSS_SELECTOR, value=self.output_css)

    def close(self):
        self.driver.quit()

    def translate(self, input_text):
        self.input_area.clear()

        self.sentence_list = []
        # do not translate short text
        if (len(input_text) < self.lowthresh):
            return ''
        if (len(input_text) > self.maxlength):
            self.split_to_sentence += re.split("(?<=[.!?])\s+", input_text)
            self.i = 0
            for self.onesentence in self.split_to_sentence:
                if (len(self.onesentence) + len(self.sentence_list[self.i]) > self.maxlength):
                    self.sentence_list.append('')
                    self.i += 1
                self.sentence_list[self.i] += self.onesentence
        else:
            self.sentence_list = [input_text]

        for self.element_text in self.sentence_list:
            clipboard.copy(self.element_text)
            self.input_area.send_keys(Keys.CONTROL, 'v')

    # Wait for translation to appear on the web page
            self.content = ''
            while True:
                self.content += self.output_area.get_property('value')
                if (len(self.content) == 0 ):
                    time.sleep(1)
                else:
                    break

        return self.content


    def refresh(self):
        self.nowtime = time.time()
        # print("deepl refresh")
        #if elapsed time is longer than threshold then restart
        if (self.nowtime - self.starttime > self.threshtime):
            #print("Deepl refresh")
            self.close()
            self.open()
#        print (time.strftime("%T:%M:%S%p \r\n", time.localtime(nowtime)))
