# Installing selnium
pip install selenium

# import Pandas
import pandas as pd

# Import Splinter and BeautifulSoupa
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Set up Splinter
executable_path = {'executable_path' : ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#### Assigning the url and instructing the browser to visit it. Searching for elements with specific combination of tag div and attribute list_text. Telling the browser to wait 1 second before searching for components. 

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Assigning slide_elem as the variable to look for the div and its descendent (the other tags within the div element).  The dot (.) is used for selecting classes such as list_text, so div.list_text pinspoints the div tag with the class of list_text.  CSS goes from right to left, so the last item of the list will be returned first. Because of ths when using select_one, the first matching element returned will be li element with a class of slide and all nested elements. 
# Setting up the HTML parser. 
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# We chain .find onto variable slide_elem.  This way we are saying this variable holds lot of information so look inside of that information to find this specific data (the content title, which we specified by div with a class of content_title. 
slide_elem.find('div', class_='content_title')

# The " < a>" element's most important attribute is the href attribute, which indicates the link's destination. The .get_text() method added to the .find() method returns only the texte of the element. For example, only the tittl not any of the HTML tags or elements. 
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# To get summary text of the article we need to change the attributte to to div and class=article_teaser_body
# As there are many articles which a tag of div and a class of article_teaser_body. We want to pull the most recent one (normally is the first one on the list).  Using find() method. 
# Use the parent element to find the paragraph text. 

news_p = slide_elem.find('div',class_='article_teaser_body').get_text()
news_p

### Featured Images
# Setting up the URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button.  full_image_elem is the variable to hold the scraped image.
# With .click splinter will click the image to view its full size. With .find() the browser will find an element by its tag.
# With the indexing 1 the browser will automatically click the second button and change the view to a slideshow of images. 
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# With the new page loaded onto the automated browser,it needs to be parsed to continue and scrape the full size image URL
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Finding the relative image URL. Using img and fancybox-img to build the URL to the full-size image. 
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# Scraping the entire table with Pandas .read_html() function.
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description','Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()
  # Ending the automated browsing session.
browser.quit()






