# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime 
from selenium.webdriver.common.keys import Keys
import json
from pprint import pprint
import requests
from time import sleep

class AutoreportSpider(CrawlSpider):
    name = 'autoreport'
    
    def start_requests(self):
        with open('data.json') as f:
            json_data = json.load(f)
        company = json_data['company']
        address = json_data['address']
        city = json_data['city']
        state = json_data['state']
        zipcode = json_data['zipcode']
        telephone = json_data['telephone']
        savepath = json_data['BASE_DIR']+'/hello/static/'+json_data['Image_DIR']+'/'
        courl = json_data['url']

        gispeedm = None
        gispeedd = None
        pinggrade = None
        pingsize = None
        pingtime = None
        pingreq = None
        goreview = None
        loreview = None
        lopercent = None
        gtspeed = None
        gtyslow = None
        gtloadtime = None
        gtpagesize = None
        gtrequest = None
        jsonStatus = {
        'GIMStatus' : 'started',
        'GIDStatus' : 'started',
        'PGStatus' : 'started',
        'GTStatus' : 'started',
        'GOGStatus' : 'started',
        'LOStatus' : 'started',
        'status' : 'started'
        }

        data = ['https://developers.google.com/speed/pagespeed/insights/?url='+courl+'&tab=mobile','https://developers.google.com/speed/pagespeed/insights/?url='+courl+'&tab=desktop','https://tools.pingdom.com/','https://gtmetrix.com/','https://www.google.com/','https://www.optimizelocation.com/partner/monopolydigital/diagnostic.html']
        chrome_driver = "scrapy_app/chromedriver/chromedriver.exe"
        options = Options()
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary
        browser = webdriver.Chrome(chrome_driver, chrome_options = options)
        browser.set_window_size(1920, 1680)
        browser.set_page_load_timeout(30)
        browser.maximize_window()

        with open(savepath+'data.json', 'w') as outfile:
            json.dump(jsonStatus, outfile)

        for index, url in enumerate(data):
            try:
                browser.get(data[index])
            except:
                print(data[index] + ' took too long')
            else:
                # where images saved
                if index == 0:
                    while True:
                        sleep(1)
                        try:
                            gispeedm = browser.find_elements_by_xpath('//*[@id="page-speed-insights"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div/a/div[1]')[0].text
                        except:
                            jsonStatus['GIMStatus'] = 'pending'
                            with open(savepath+'data.json', 'w') as outfile:
                                json.dump(jsonStatus, outfile)
                            pprint(gispeedm)
                        else: 
                            break
                        pass
                    pprint(gispeedm)
                    jsonStatus['GIMStatus'] = 'finished'
                    with open(savepath+'data.json', 'w') as outfile:
                        json.dump(jsonStatus, outfile)
                    browser.save_screenshot(savepath+'screenshot' + str(index) + '.png')
                if index ==1:
                    while True:
                        sleep(1)
                        try:
                            gispeedd = browser.find_elements_by_xpath('//*[@id="page-speed-insights"]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div/a/div[1]')[0].text
                        except:
                            jsonStatus['GIDStatus'] = 'pending'
                            with open(savepath+'data.json', 'w') as outfile:
                                json.dump(jsonStatus, outfile)
                            pprint(gispeedd)
                        else:
                            break
                        pass
                    pprint(gispeedd)
                    jsonStatus['GIDStatus'] = 'finished'
                    with open(savepath+'data.json', 'w') as outfile:
                        json.dump(jsonStatus, outfile)
                    browser.save_screenshot(savepath+'screenshot' + str(index) + '.png')
                if index == 2:
                    browser.find_element_by_id('urlInput').send_keys(courl)
                    submit_button = browser.find_elements_by_xpath('/html/body/app-root/main/app-home-hero/header/section/app-test-runner/div/div[2]/div[3]/input')[0]
                    submit_button.click()
                    while True:
                        sleep(1)
                        try:
                            pinggrade = browser.find_elements_by_xpath('/html/body/app-root/main/app-report/section[1]/app-summary/div/div/app-summary-player/div/div[2]/div/div[1]/app-metric/div[2]')[0].text
                        except:
                            jsonStatus['PGStatus'] = 'pending'
                            with open(savepath+'data.json', 'w') as outfile:
                                json.dump(jsonStatus, outfile)
                            pprint(pinggrade)
                        else:
                            break
                        pass
                    sleep(10)
                    pingsize = browser.find_elements_by_xpath('/html/body/app-root/main/app-report/section[1]/app-summary/div/div/app-summary-player/div/div[2]/div/div[2]/app-metric/div[2]')[0].text
                    pingtime = browser.find_elements_by_xpath('/html/body/app-root/main/app-report/section[1]/app-summary/div/div/app-summary-player/div/div[2]/div/div[3]/app-metric/div[2]')[0].text
                    pingreq = browser.find_elements_by_xpath('/html/body/app-root/main/app-report/section[1]/app-summary/div/div/app-summary-player/div/div[2]/div/div[4]/app-metric/div[2]')[0].text
                    pprint(pinggrade)
                    jsonStatus['PGStatus'] = 'finished'
                    with open(savepath+'data.json', 'w') as outfile:
                        json.dump(jsonStatus, outfile)
                    browser.save_screenshot(savepath+'screenshot' + str(index) + '.png')
                if index == 3:
                    gturlinput = browser.find_elements_by_xpath('/html/body/div[1]/main/article/section[1]/div/form/div/div[1]/div/input')[0]
                    gturlinput.send_keys(courl)
                    gtsubmitbtn = browser.find_elements_by_xpath('/html/body/div[1]/main/article/section[1]/div/form/div/div[2]/button')[0]
                    gtsubmitbtn.click()
                    while True:
                        sleep(1)
                        try:
                            gtspeed = browser.find_elements_by_xpath('/html/body/div[1]/main/article/div[2]/div[1]/div/div[1]/span/span')[0].text
                        except:
                            jsonStatus['GTStatus'] = 'pending'
                            with open(savepath+'data.json', 'w') as outfile:
                                json.dump(jsonStatus, outfile)
                            pprint(gtspeed)
                        else:
                            break
                        pass
                    sleep(10)
                    gtyslow = browser.find_elements_by_xpath('/html/body/div[1]/main/article/div[2]/div[1]/div/div[2]/span/span')[0].text
                    gtloadtime = browser.find_elements_by_xpath('/html/body/div[1]/main/article/div[2]/div[2]/div/div[1]/span')[0].text
                    gtpagesize = browser.find_elements_by_xpath('/html/body/div[1]/main/article/div[2]/div[2]/div/div[2]/span')[0].text
                    gtrequest = browser.find_elements_by_xpath('/html/body/div[1]/main/article/div[2]/div[2]/div/div[3]/span')[0].text
                    pprint(gtspeed)
                    jsonStatus['GTStatus'] = 'finished'
                    with open(savepath+'data.json', 'w') as outfile:
                        json.dump(jsonStatus, outfile)
                    browser.save_screenshot(savepath+'screenshot' + str(index) + '.png')
                if index == 4:
                    goginput = browser.find_elements_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[1]/input')[0]
                    goginput.send_keys(company+" reviews")
                    goginput.send_keys(Keys.ENTER)
                    jsonStatus['GOGStatus'] = 'pending'
                    with open(savepath+'data.json', 'w') as outfile:
                        json.dump(jsonStatus, outfile)
                    sleep(5)
                    jsonStatus['GOGStatus'] = 'finished'
                    with open(savepath+'data.json', 'w') as outfile:
                        json.dump(jsonStatus, outfile)
                    browser.save_screenshot(savepath+'screenshot' + str(index) + '.png')
                if index == 5:
                    locompanyinput = browser.find_elements_by_xpath('//*[@id="scan-name"]')[0]
                    locompanyinput.send_keys(company)
                    loaddressinput = browser.find_elements_by_xpath('//*[@id="scan-address"]')[0]
                    loaddressinput.send_keys(address)
                    locityinput = browser.find_elements_by_xpath('//*[@id="scan-city"]')[0]
                    locityinput.send_keys(city)
                    lostateinput = browser.find_elements_by_xpath('//*[@id="scan-state"]')[0]
                    lostateinput.send_keys(state)
                    lozipinput = browser.find_elements_by_xpath('//*[@id="scan-zip"]')[0]
                    lozipinput.send_keys(zipcode)
                    lophoneinput = browser.find_elements_by_xpath('//*[@id="scan-phone-fullLine"]')[0]
                    lophoneinput.send_keys(telephone)
                    loclickbtn = browser.find_elements_by_xpath('//*[@id="scan-submit"]')[0]
                    loclickbtn.click()
                    
                    lotxt = None
                    while True:
                        sleep(1)
                        try:
                            lotxt = browser.find_elements_by_xpath('//*[@id="location-details-container"]/div/div[2]/div/p[1]')[0].text
                        except:
                            pprint(lotxt)
                            jsonStatus['LOStatus'] = 'pending'
                            with open(savepath+'data.json', 'w') as outfile:
                                json.dump(jsonStatus, outfile)
                        else:
                            if lotxt != '':
                                break
                        pass
                    pprint(lotxt)
                    sleep(5)
                    loreview = browser.find_elements_by_xpath('//*[@id="scan-summary"]/div[1]/div/div/div[2]/div[2]/span')[0].text
                    lopercent = browser.find_elements_by_xpath('//*[@id="scan-summary"]/div[1]/div/div/div[2]/div[1]/span')[0].text
                    jsonStatus['LOStatus'] = 'finished'
                    with open(savepath+'data.json', 'w') as outfile:
                        json.dump(jsonStatus, outfile)
                    browser.save_screenshot(savepath+'screenshot' + str(index) + '.png')
                #if index == 6:
                    #API_KEY = '2e952b8c40a911f15c59c5a29715aa56'  # Your 2captcha API KEY
                    #site_key = '6LdkDiYUAAAAADfP_-3ZL5sXDaHMCMt0AUzzTts6'  # site-key, read the 2captcha docs on how to get this
                    #site_url = 'https://testmysite.thinkwithgoogle.com/'  # example url

                    #s = requests.Session()
                    #captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(API_KEY, site_key, url)).text.split('|')[1]

                    #recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
                    #print("solving ref captcha...")
                    #while 'CAPCHA_NOT_READY' in recaptcha_answer:
                    #    sleep(5)
                    #    recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
                    #recaptcha_answer = recaptcha_answer.split('|')[1]
                    #pprint(recaptcha_answer)

                    #jdata = {
                    #'recaptcha_answer':str(recaptcha_answer)
                    #}

                    #with open(savepath+'data.json', 'w') as outfile:
                    #    json.dump(jdata, outfile)


                    #recaptcha_answer = "03ADlfD18ocvcF4HtzdKTr-bWM36dCzl23M30s2wGpB5XN3NMRJETunzDqtaS0ReRhbRptn-GZ802IyZWRwQvIvTol8adL1MehiaMezxGaQhew1ChMloIcjdxEKPyNhD3hcBzRDqN7VYZVsynF0pZeQ84TzwvarxmGX4jF5V67SL9Q6PbHpH83tAO70ZXj5jRjCBt5UCv1nZslwMS-5q8aBOF1vAW16SDNzkbQNticvqMpfMorxWu7bGyjA0bk_u3W4GX6ZnSn3dUPwNcvodrTxOx_B4Ftq46dlmXCAhVV238madVB6kRDoRhxq5AdzSzCWjOP4D96_eJ6XVLFXioKG7MZdUZabcxeN2RJZtn1wMkZ-wdTi-_v4r8QrFH69ojsBpHdM0oUF9Qe"
                    #strscript = 'document.getElementById("g-recaptcha-response").innerHTML='+'"'+str(recaptcha_answer)+'"'+';'
                    #while (datetime.now()-t1).seconds <= 30:
                    #    pass
                    #browser.execute_script(strscript)
                    #browser.execute_script('document.getElementsByClassName("url-entry__form")[0].submit();')

                    #tginput = browser.find_elements_by_xpath('//*[@id="content"]/main/div[2]/div[2]/div/div[3]/form/input[2]')[0]
                    #tginput.send_keys('http://ojedashowerpans.com/')

                    #while True:
                    #    pass
                    #tgbutton = browser.find_elements_by_xpath('//*[@id="content"]/main/div[2]/div[2]/div/div[3]/form/button')[0].click()
                    

                    #while (datetime.now()-t1).seconds <= 80:
                    #    pass
                    #browser.save_screenshot(savepath+'screenshot' + str(index) + '.png') 
        
        jtdata = {
        'gispeedm':str(gispeedm),
        'gispeedd':str(gispeedd),
        'pinggrade':str(pinggrade),
        'pingsize':str(pingsize),
        'pingtime':str(pingtime),
        'pingreq':str(pingreq),
        'loreview':str(loreview),
        'lopercent':str(lopercent),
        'gtspeed':str(gtspeed),
        'gtyslow':str(gtyslow),
        'gtloadtime':str(gtloadtime),
        'gtpagesize':str(gtpagesize),
        'gtrequest':str(gtrequest)
        }
        jsonStatus.update(jtdata)
        jsonStatus['status'] = 'finished'
        with open(savepath+'data.json', 'w') as outfile:
            json.dump(jsonStatus, outfile)
        browser.quit()

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
