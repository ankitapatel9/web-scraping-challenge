# Dependencies
# --------------------------------------------------------------------------
import pandas as pd
import os
import requests
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# --------------------------------------------------------------------------
# navigation to chrome website
executable_path = {'executable_path': 'chromedriver.exe'}
browser =  Browser('chrome', **executable_path, headless=False)

# --------------------------------------------------------------------------
# define one fuction scrape that has all dict.
# --------------------------------------------------------------------------    
def scrape():
    scraped_data = {}
    news_output = mars_news()
    scraped_data["mars_news"] = news_output[0]
    scraped_data["mars_paragraph"] = news_output[1]
    scraped_data["mars_image"] = mars_image()
    scraped_data["mars_weather"] = mars_weather()
    scraped_data["mars_facts"] = mars_facts()
    scraped_data["mars_hemisphere"] = mars_hem_data()

    return scraped_data

#--------------------------------------------------------------------------
# Mars News Title and Paragraph

def mars_news():
    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #  getting latest news title and paragraph from nasa news url
    news_title = soup.find("div",class_="content_title").text
    print(f"News Title: {news_title}")
    news_p = soup.find("div", class_="article_teaser_body").text
    print(f"News Paragraph: {news_p}")
    news_output = [news_title, news_p]
    return news_output

#---------------------------------------------------------------------------
# ### JPL Mars Space Images - Featured Image
# --------------------------------------------------------------------------

def  mars_image():
    space_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(space_image_url)
    #  Use splinter to navigate the site and find the image url for the current Featured Mars Image
    # full_image = browser.find_by_id("full_image")
    #pause 2 seconds to let it load
    # time.sleep(1)
    space_image_html = browser.html
    soup = BeautifulSoup(space_image_html,"html.parser")
    image = soup.find('img', class_ = 'thumb')['src']
    featured_image_url = "https://www.jpl.nasa.gov" + image
    print(f"Space Image URL : {featured_image_url}")
    return featured_image_url

#------------------------------------------------------------------------------
# ### Mars Weather
# -----------------------------------------------------------------------------
 
def mars_weather():
    # scrape the latest Mars weather tweet
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')
    #  Save the tweet text for the weather report as a variable called
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(f"Mars Weather Tweet : {mars_weather}")
    return mars_weather

#------------------------------------------------------------------------------
# ### Mars Facts
# -----------------------------------------------------------------------------

def  mars_facts():
    mars_fact_url = "https://space-facts.com/mars/"
    mars_table = pd.read_html(mars_fact_url)
    df = mars_table[0]
    df.columns = ['facts', 'values']
    df.head(15)
    mars_facts = df.to_html(index = False)
    # print(mars_facts)
    return mars_facts

#------------------------------------------------------------------------------
# ### Mars Hemispheres
# -----------------------------------------------------------------------------


def mars_hem_data():
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    hemisphere_html = browser.html
    soup = BeautifulSoup(hemisphere_html, 'html.parser')
    hemisphere_list = []
    category = soup.find("div", class_ = "result-list" )
    hemispheres =category.find_all("div", class_="item")
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.strip("Enhanced")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        hemisphere_html = browser.html
        soup = BeautifulSoup(hemisphere_html, 'html.parser')
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_list.append({"title": title, "img_url": image_url})
    return hemisphere_list  