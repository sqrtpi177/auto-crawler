import os
import webbrowser as wb

from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import urllib.parse
import time
from selenium.webdriver.common.keys import Keys


def get_images(keyword):
    search_item = keyword
    driver_path = './chromedriver.exe'
    folder = './data'

    url = "https://www.google.com/search"
    size = 300
    params = {
        'q': search_item,
        'tbm': 'isch',
        'sa': '1',
        'source': 'lnms&tbm=isch'
    }
    url = url + '?' + urllib.parse.urlencode(params)
    user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument(user_agent)
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(driver_path, options=options)
    time.sleep(0.5)
    driver.get(url)
    html = driver.page_source
    time.sleep(0.5)

    # scroll down to reveal images
    soup_temp = BeautifulSoup(html, 'html.parser')
    elem_body = driver.find_element_by_tag_name("body")
    img_cnt = 0
    img4page = 0
    while img_cnt < size * 10:
        elem_body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        img4page = len(soup_temp.find_all("img")) - img4page
        img_cnt += img4page

    print("%d images" % img_cnt)

    # parse html and extract src
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find_all("img")

    file_num = 0
    src_url = []
    for line in img:
        if str(line).find('data-src') != -1 and str(line).find('http') < 100:
            src_url.append(line['data-src'])
            file_num += 1

    # save images
    save_dir = os.path.join(folder, search_item, 'images')
    try:
        if not os.path.isdir(save_dir):
            os.makedirs(os.path.join(save_dir))
    except OSError as e:
        print(e)
        print("failed to create directory")

    for i, src in zip(range(file_num), src_url):
        urllib.request.urlretrieve(src, save_dir + '/' + search_item + '-' + str(i + 1) + '.jpg')

    print("saved images")

    driver.quit()

    # open in file explorer
    path = os.path.join(os.getcwd(), folder)
    wb.open(os.path.realpath(path))
