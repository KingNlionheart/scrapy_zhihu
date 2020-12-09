from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-background-networking")
options.add_argument("--disable-default-apps")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-sync")
options.add_argument("--disable-translate")
options.add_argument("--hide-scrollbars")
options.add_argument("--metrics-recording-only")
options.add_argument("--mute-audio")
options.add_argument("--no-first-run")
options.add_argument("--safebrowsing-disable-auto-update")

driver = webdriver.Remote(

            command_executor="http://192.168.50.16:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME,
            options=options,
        )



def my_parser(html):

    soup = BeautifulSoup(html, 'html.parser')


    video_detial=soup.find('ul',class_='clearfix cube-list').find('li')
    text={"title":video_detial.find('a',class_='title').text,
           "date":video_detial.find('span',class_='time').text}


    print(text)

def get_data(url='https://space.bilibili.com/8730238/video'):

    start_time=time.time()
    driver.get(url)
    end_time=time.time()
    print("{0:.02f}s  ".format(end_time-start_time),end='')

    time.sleep(10)

    print(driver.title)
    try:
        my_parser(driver.page_source)
    except Exception as e:
        print(type(e))
    driver.delete_all_cookies()

get_data()

driver.close()
driver.quit()