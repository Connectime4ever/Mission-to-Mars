#!/usr/bin/env python
# coding: utf-8

# In[59]:


pip install selenium


# In[64]:


# import Pandas
import pandas as pd


# In[65]:


# Import Splinter and BeautifulSoupa
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# In[66]:


executable_path = {'executable_path' : ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# #### Assigning the url and instructing the browser to visit it. Searching for elements with specific combination of tag div and attribute list_text. Telling the browser to wait 1 second before searching for components. 

# In[5]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# ###### Assigning slide_elem as the variable to look for the div and its descendent (the other tags within the div element).  The dot (.) is used for selecting classes such as list_text, so div.list_text pinspoints the div tag with the class of list_text.  CSS goes from right to left, so the last item of the list will be returned first. Because of ths when using select_one, the first matching element returned will be li element with a class of slide and all nested elements. 

# In[6]:


# Setting up the HTML parser. 
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# ###### We chain .find onto variable slide_elem.  This way we are saying this variable holds lot of information so look inside of that information to find this specific data (the content title, which we specified by div with a class of content_title. 

# In[7]:


slide_elem.find('div', class_='content_title')


# ##### The " < a>" element's most important attribute is the href attribute, which indicates the link's destination. The .get_text() method added to the .find() method returns only the texte of the element. For example, only the tittl not any of the HTML tags or elements. 

# In[8]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# ##### To get summary text of the article we need to change the attributte to to div and class=article_teaser_body
# ##### As there are many articles which a tag of div and a class of article_teaser_body. We want to pull the most recent one (normally is the first one on the list).  Using find() method. 

# In[9]:


# Use the parent element to find the paragraph text. 

news_p = slide_elem.find('div',class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[10]:


# Setting up the URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[11]:


# Find and click the full image button.  full_image_elem is the variable to hold the scraped image.
# With .click splinter will click the image to view its full size. With .find() the browser will find an element by its tag.
# With the indexing 1 the browser will automatically click the second button and change the view to a slideshow of images. 

full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[12]:


# With the new page loaded onto the automated browser,it needs to be parsed to continue and scrape the full size image URL
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[13]:


# Finding the relative image URL. Using img and fancybox-img to build the URL to the full-size image. 
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[14]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[15]:


# Scraping the entire table with Pandas .read_html() function.
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description','Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[16]:


df.to_html()


# In[17]:


# Ending the automated browsing session.
browser.quit()


# ### Challenge starter code

# In[18]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[19]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[20]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[21]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[22]:


slide_elem.find('div', class_='content_title')


# In[23]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[24]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[25]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[26]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[27]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[28]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[29]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[30]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[31]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[32]:


df.to_html()


# ### D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ##### Hemispheres

# In[88]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[107]:


# 2. Create a list to hold the images and titles.

hemisphere_image_urls = []                     


# In[108]:


for i in range(1,5):
    x_path= '//*[@id="product-section"]/div[2]/div[' + str(i)+ ']/div/a/h3'
    browser.find_by_xpath(x_path).click()
    
    img_url = browser.find_by_xpath('//*[@id="wide-image"]/div/ul/li[1]/a')['href']
    title = browser.find_by_xpath ('//*[@id="results"]/div[1]/div/div[3]/h2').text
   
    hemisphere_image_urls.append({
        'img_url':img_url,
        'title':title
        
    })
   

    browser.back()


# In[109]:


hemisphere_image_urls 


# In[110]:


# 5. Quit the browser
browser.quit()


# In[ ]:




