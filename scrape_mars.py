from splinter import Browser
from bs4 import BeautifulSoup
import pymongo
import time
import re
import pandas as pd

def init_browser():
    # Initialize executable path for the chromedriver
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
def scrape_info():

    browser = init_browser()
     
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    time.sleep(0.5)
    html_1 = browser.html
    soup = BeautifulSoup(html_1, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    # print (news_title.text)
    news_para = soup.find('div', class_='article_teaser_body').text
    # print (news_para.text)

    jpl_nasa_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_nasa_url)
    time.sleep(0.5)
    browser.click_link_by_id('full_image')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(0.5)
    html_2 = browser.html
    soup = BeautifulSoup(html_2, 'html.parser')
    images = soup.find_all('div', class_="download_tiff")
    for img in images:
        try:
            image_1 = img.a
            image_2 = image_1['href']
    #         print(image_2)
            if image_2.endswith('jpg'):
                featured_image_url = image_2
    #             print(featured_image_url)
                break
        except AttributeError as e:
            print(e)

    mars_weather_twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_twitter_url)
    time.sleep(0.5)
    html_3 = browser.html
    soup = BeautifulSoup(html_3, 'html.parser')
    if soup.find(href=re.compile("MarsWxReport")):
        mars_twitter_post = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
        mars_weather_twitter_post = mars_twitter_post.contents[0]
    #     print(mars_weather_twitter_post)

    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)
    time.sleep(0.5)
    html_4 = browser.html
    soup = BeautifulSoup(html_4, 'html.parser')
    facts_table = soup.find('table')
    column1 = facts_table.find_all('td', class_='column-1')
    column2 = facts_table.find_all('td', class_='column-2')
    Parameters = []
    Values = []
    for row in column1:
        parameter = row.text.strip(":")
        Parameters.append(parameter)
    for row in column2:
        value = row.text.strip()
        Values.append(value)

    mars_facts = pd.DataFrame({"Parameter": Parameters, "Value": Values})
    mars_facts_html = mars_facts.to_html(header=False, index=None)
    # print (mars_facts)

    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemispheres_url)
    time.sleep(0.5)
    html_5 = browser.html
    soup = BeautifulSoup(html_5, 'html.parser')
    hemisphere_image_urls = []
    base_url = "https://astrogeology.usgs.gov"
    links = soup.find_all('div', class_="description")
    for link in links:
        time.sleep(0.5)
        title = link.h3.text
    #     print (title)
        new_link = base_url + str(link.a['href'])
    #     print(new_link)
        browser.visit(new_link)
        time.sleep(0.5)
        browser.click_link_by_partial_href('#open')
        time.sleep(0.5)
        html_6 = browser.html
        soup = BeautifulSoup(html_6, 'html.parser')
        full_img = soup.find('img', class_='wide-image')
        img_link = full_img['src']
    #     print(img_link)
        full_img_link = base_url + img_link
    #     print(full_img_link)
        hemisphere_image_urls.append({'title': title, 'img_url': full_img_link})
        browser.back()
    # hemisphere_image_urls
    browser.quit()

    mars_scraped_data = {
        'Mars_Headlines' : news_title,
        'Mars_News_Details' : news_para,
        'Mars_Space_Image' : featured_image_url,
        'Mars_Weather_Report' : mars_weather_twitter_post,
        'Mars_Facts' : mars_facts_html,
        'Mars_Hemispheres' : hemisphere_image_urls
        }
    print (mars_scraped_data)

    return(mars_scraped_data)
