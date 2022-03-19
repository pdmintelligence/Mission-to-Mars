#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

#importing pandas*.
import pandas as pd


# In[2]:


#creating browser and unpacking the dictioanry path (**)

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


#set up HTML parser*. 
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


#chaining find onto previously assigned variable*. 
slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ###Featured Images

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ##Scraping Mars Facts Data

# In[13]:


#when sraping tables, simply scrape the whole table and inject it into a dataframe with pandas*.
#pandas read_html() specifically searches for and returns tables found in HTML*.
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


#testing conversion of extracted dataframe into HTML format*.
df.to_html()


# In[15]:


#exiting application
browser.quit()


# ##D1 Scrape High Resolution Mars' Hemisphere Images and Titles

# #Hemispheres


#importing dependencies for this challenge project*.
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager


#creating browser and unpacking the dictioanry path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)



# 1. Use browser to visit the URL 
#The original URL text linked to 'marshemispheres; however, the link directs elsewhere*.
#coded out and replaced --url = 'https://marshemispheres.com/'

#prepping for scrapes*.
url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

#converting browser html into soup object*.
html = browser.html
soup = bs(html, "html.parser")

#returning results as iterable list*.
results=soup.find_all('div',class_='item')


# 2 Create a list to hold the images and titles.
hemisphere_image_urls = []




for item in results:
    
    #getting image links*.
    href = item.find('a', class_='itemLink product-item')
    link = "https://astrogeology.usgs.gov" + href['href']
    browser.visit(link)
    
    #creating new soup after click*. 
    click_html=browser.html
    click_soup = bs(click_html, "html.parser")
    #returning results as iterable list*.
    click_results=click_soup.find('div',class_='downloads').find('a')['href']

    #gatting titles*.
    title=item.find('h3').text
    title=title.replace("Enhanced","")
    hemisphere_image_urls.append({"title":title,"img_url":click_results})
    
    #iterating back*
    browser.back()




# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()