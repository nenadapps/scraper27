import requests
from bs4 import BeautifulSoup
import datetime
from random import shuffle

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(html, scrape_date):
    
    stamp = {}
    
    try:
        price = html.select('td')[-1].get_text().strip()
        price = price.replace('$', '').strip()
        stamp['price'] = price
    except:
        stamp['price'] = None 
    
    try:
        image = html.select('a')[0].get('href')
        stamp['image'] = image
    except: 
        stamp['image'] = None

    try:
        catalogue = html.select('td')[1].get_text().strip()
        stamp['catalogue'] = catalogue
    except:
        stamp['catalogue'] = None
        
    try:
        cat_price = html.select('td')[2].get_text().strip()
        stamp['cat_price'] = cat_price
    except:
        stamp['cat_price'] = None   
        
    try:
        raw_text_cont = html.select('p')[0]
        raw_text = raw_text_cont.select('a')[-1].get_text().strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None
        
    stamp['currency'] = "USD"
        
    stamp['scrape_date'] = scrape_date
    
    print(stamp)
    print('+++++++++++++')
           
    return stamp

def get_page_items(url):

    items = []
    scrape_date = ''

    try:
        html = get_html(url)
    except:
        return items, scrape_date
    
    try:
        scrape_date = html.find_all('span', {'style': 'font-size:40.0pt;font-family:"Arial","sans-serif";color:black'})[2].get_text().strip()
        scrape_date = scrape_date.replace('st,', '').replace('nd,', '').replace('th,', '').replace('\n', ' ')
        date_time_obj = datetime.datetime.strptime(scrape_date, '%B %d %Y')
        scrape_date = str(date_time_obj.date())
    except:
        pass

    try:
        for item in html.select('.MsoNormalTable tr'):
            td4 = item.select('td')[4].get_text().strip()
            td_last = item.select('td')[-1].get_text().strip()
            if ((item not in items) and (td4 != 'Buyer #') and td_last):
                items.append(item)
    except:
        pass
   
    shuffle(list(set(items)))
    
    return items, scrape_date

def get_page_urls():
    
    items = []

    url = 'http://www.fvhstamps.com/PWA/FvhWAPR.htm'

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item in html.select('p.MsoNormal b span a'):
            item_link = item.get('href')
            if item_link not in items:
                items.append(item_link)
    except: 
        pass
    
    shuffle(items)
    
    return items

page_urls = get_page_urls()
for page_url in page_urls:
    page_items, scrape_date = get_page_items(page_url)
    for page_item in page_items:
        stamp = get_details(page_item, scrape_date)
