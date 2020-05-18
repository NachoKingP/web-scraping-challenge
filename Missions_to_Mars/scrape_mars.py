# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 
import time

def init_browser(): 
    # Replace the path with your actual path to the chromedriver

    #Mac Users
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #return Browser('chrome', **executable_path, headless=False)

    #Windows Users
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# Create dictionary for returning mars information after scraping
mars_info = {}

# Scrape Mars News
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()

        # Set URL to NASA Mars News website
        news_url = 'https://mars.nasa.gov/news/'
        browser.visit(news_url)
        time.sleep(5)

        # Create HTML Object and parse HTML with Beautiful Soup
        html_news = browser.html
        soup = BeautifulSoup(html_news, 'html.parser')


        # Scrape data from the title and p tags
        text_tag = soup.find('div', class_='list_text')
        title = text_tag.find('div', class_='content_title')
        article_title = title.find('a').text
        article_p = soup.find('div', class_='article_teaser_body').text

        # Append dictionary entry from Mars News Source
        mars_info['news_title'] = article_title
        mars_info['news_paragraph'] = article_p

        return mars_info

    finally:

        browser.quit()

# Scrape Mars Featured Image
def scrape_mars_image():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Set URL to JPL website
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        image_url_prefix = 'https://jpl.nasa.gov'
        browser.visit(image_url_featured)
        time.sleep(5)

        # Create HTML Object and parse HTML with Beautiful Soup 
        html_image = browser.html
        soup = BeautifulSoup(html_image, 'html.parser')

        # Retrieve background-image url from style tag 
        image_carousel = soup.find('article', class_='carousel_item')
        footer = image_carousel.find('footer')
        link_url = footer.find('a')["data-fancybox-href"]

        # Concatenate website url with scrapped route
        featured_image_url = image_url_prefix + link_url

        # Display full link to featured image
        featured_image_url 

        # Dictionary entry from FEATURED IMAGE
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info
    finally:

        browser.quit()

# Scrape Mars Weather 
def scrape_mars_weather():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Set URL to Mars Weather Twitter
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)
        time.sleep(5)

        # Create HTML Object and parse HTML with Beautiful Soup 
        html_weather = browser.html
        soup = BeautifulSoup(html_weather, 'html.parser')

        # Find all tweets through BS
        latest_tweet = soup.find('article', role="article")
        mars_weather = latest_tweet.find_all('span')[4].text

        # Dictionary entry from WEATHER TWEET
        mars_info['mars_weather'] = mars_weather
        
        return mars_info
    finally:

        browser.quit()


# Scrape Mars Facts
def scrape_mars_facts():

    # Set URL to Mars Facts website
    facts_url = 'http://space-facts.com/mars/'

    # Parse the URL using Pandas
    mars_facts = pd.read_html(facts_url)

    # Find the table containing the Mars Facts and assign it to mars_df
    mars_df = mars_facts[0]

    # Label the columns
    mars_df.columns = ['Description','Value']

    # Reassign index to the `Description` column
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html()

    # Dictionary entry from MARS FACTS
    mars_info['mars_facts'] = data

    return mars_info


# Scrape Mars Hemispheres Images
def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Set URL to usgs.gov website
        hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemisphere_url)
        time.sleep(5)

        # Create HTML Object and parse HTML with Beautiful Soup
        html_hemisphere = browser.html
        soup = BeautifulSoup(html_hemisphere, 'html.parser')

        # Declare list variables for storing image URLs dictionary
        hemisphere_image_urls = []
        hemisphere_url_prefix = 'https://astrogeology.usgs.gov'

        # Retreive all items that contain Mars Hemispheres data
        items = soup.find_all('div', class_='item')

        # Loop through the items
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemisphere_url_prefix + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemisphere_url_prefix + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

        mars_info['hemisphere_image_urls'] = hemisphere_image_urls

        
        # Return mars_data dictionary 

        return mars_info
    finally:

        browser.quit()

