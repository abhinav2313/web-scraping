import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd
import requests

def init_browser():
    executable_path = {'executable_path': '/Users/abhsharm/Softwares/Drivers/chromedriver'}
    return Browser('chrome', **executable_path, headless= False)

def scrape():
    browser = init_browser()

    the_data = {}

    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
    time.sleep(2)

    html = browser.html
    soup_news = bs(html, 'html.parser')

    results_news = soup_news.find_all('div', class_="slide")

    for result in results_news:
        news_title = result.find('div', class_='content_title').text
        news_p = result.find('div', class_='rollover_description_inner').text

        the_data['news_title'] = news_title
        the_data['report'] = news_p
    

    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_img)
    time.sleep(2)

    html = browser.html
    soup_img = bs(html, 'html.parser')

    results_img = soup_img.find_all('div', class_='carousel_container')

    for result in results_img:
        featured_img = result.find('a', class_='button fancybox')['data-fancybox-href']
        url_ext = 'https://www.jpl.nasa.gov'
        featured_image_url = url_ext+featured_img

        the_data['src'] = featured_image_url

    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    time.sleep(2)

    html = browser.html
    soup_weather = bs(html, 'html.parser')

    weather = soup_weather.find('p', class_='tweet-text').text

    the_data['weather'] = weather
    
    url_facts = 'https://space-facts.com/mars/'
    browser.visit(url_facts)
    time.sleep(2)

    html = browser.html
    soup_facts = bs(html, 'html.parser')

    results_facts = soup_facts.find_all('div', id='facts')

    for result in results_facts:
        text_facts = result.text

        the_data['facts'] = text_facts

    url_hemis = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemis)
    time.sleep(2)

    html = browser.html
    soup_hemis = bs(html, 'html.parser')

    imgs = soup_hemis.find_all('img', class_='thumb')
    len(imgs)

    images = []

    for i in range(0, len(imgs)):
        
        if imgs:
            a_tag = imgs[i].parent
            href = a_tag.get('href')
            url_ext = 'https://astrogeology.usgs.gov'
            img_urls = url_ext + href
            img_urls = img_urls.split()
        
        for img in img_urls:
            sub_url = img
            dir_key=sub_url.split('/')[-1].split('_')[0]
            
            browser.visit(sub_url)
            
            html = browser.html
            soup = bs(html, 'html.parser')
            
            image = {}
            sub_imgs = soup.find_all('div', class_='downloads')
            for sub_img in sub_imgs:
                the_img = sub_img.find('a')['href']
                image[dir_key]=the_img
            images.append(image)
                
        response = requests.get(the_img, stream=True)

    the_data['images'] = images
    return the_data


if __name__ == '__main__':
    scrape()
