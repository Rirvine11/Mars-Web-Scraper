from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd
import pymongo
from splinter import Browser

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    final_dict = {}
    newsurl = 'https://mars.nasa.gov/news/'
    browser.visit(newsurl)
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    jplurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jplurl)
    results = soup.find_all('carousel_items','footer')

    for result in results:
        try:
            img_url = result.find('a', class_='button fancybox')
            featured_img_url = img_url['href']
        except AttributeError as e:
            print(e)
    weatherurl = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weatherurl)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find('div', class_='js-tweet-text-container').text

    factsurl = 'https://space-facts.com/mars/'
    browser.visit(factsurl)

    tables = pd.read_html(factsurl)
    factdf = tables[0]
    factdict = factdf.to_dict(orient='records')

    hemisphereurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    browser.visit(hemisphereurl)

    found_links = soup.find('div', class_="collapsible results")
    #found_links = found_links[::2]
    found_titles = soup.find('div', class_="collapsible results")
    title = []
    for i in range(len(found_titles)):
        title.append(found_titles[i].text)

    geo_links = []
    img_url = []
    full_img = []

    for i in range(len(found_links)):
        geo_links.append(found_links[i]['href'])
        img_url.append(f'https://astrogeology.usgs.gov{geo_links[i]}')
        html = browser.visit(img_url[i])
        html = browser.html
        soup = bs(html, 'html.parser')
        html = browser.visit(img_url[i])
        html = browser.html
        soup = bs(html, 'html.parser')
        full_img.append(soup.find('a', target="_blank")['href'])


    hem_dict = {}
    hem_dict['Image'] = full_img
    hem_dict['title'] = title

    final_dict = {
        "news_title":news_title,
        "news_p":news_p,
        "featured_img":featured_img_url,
        "weather":mars_weather,
        "facts":factdict,
        "hemisphere":hem_dict

    }
    return final_dict