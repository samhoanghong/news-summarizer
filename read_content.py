import requests
from bs4 import BeautifulSoup
import yaml
import curl

#Steps: curl after getting the url from Bing API -> extract the main/body of the news

def extract_content(url):
    

    #url = 'https://www.cnn.com/2023/04/13/politics/us-government-intel-leak/index.html'
    with open('exclude_config.yaml', 'r') as f:
        classes = yaml.full_load(f)
    exclude_classes = classes['exclude_classes']
    exclude_footer = classes['exclude_div_footer']
    #print(exclude_classes)

    try:
        response = requests.get(url, timeout=10)
    
    except:
        print("Can't connect to the news page!!!!")
        return None
    html_source = response.text


    
    

    
    if (url.startswith("https://www.nytimes.com") or url.startswith("https://businessfacilities.com") ):
        soup = BeautifulSoup(curl.extract_html(url), 'html.parser')
        
    
    elif(url.startswith("https://www.bloomberg.com") or url.startswith("https://www.tribuneindia.com")):
        return None
    
    else:
        soup = BeautifulSoup(html_source, 'html.parser')

    with open("cont.txt", "w") as f:
            f.write(str(soup))

    # Find the div tag to exclude and remove it from the parsed HTML
    # exclude_tags = soup.find_all('p', class_="ssrcss-17zglt8-PromoHeadline e1f5wbog5")
    # for exclude_tag in exclude_tags:
    #    exclude_tag.extract()

    #wfla, ktla (WILL put this into 1 config file...)
    #exclude_classes = ["search-message", "screen-reader-text", "article-authors", "article-copyright", "thanks", "watch", "sailthru-signup-display-sub-message", "contact-submit"]
    
    exclude_tags = soup.find_all('p', class_=exclude_classes)
    
    for exclude_tag in exclude_tags:
       exclude_tag.extract()
    
    #exclude footer
    exclude_tags = soup.find_all('div', class_=exclude_footer)
    for exclude_tag in exclude_tags:
       exclude_tag.extract()

    exclude_tags = soup.find_all('footer')
    for exclude_tag in exclude_tags:
       exclude_tag.extract()
    
    
    ###For BBC newspaper
    #paragraph_tags = soup.find_all('div', class_="ssrcss-11r1m41-RichTextComponentWrapper")
    #paragraph_tags = soup.find_all({'div' : "ssrcss-11r1m41-RichTextComponentWrapper", "h2": "ssrcss-y2fd7s-StyledHeading e1fj1fc10"})

    #the case that we read economictimes.indiatimes.com because their main body is in div artText
    if url.startswith("https://economictimes.indiatimes.com"):
        paragraph_tags = soup.find_all("div", class_="artText")
    #timesofindia
    elif url.startswith("https://timesofindia.indiatimes.com"):
        paragraph_tags = soup.find_all("div", class_="_s30J clearfix")
        #print(paragraph_tags)
    #other news websites
    else:
        paragraph_tags = soup.find_all("p")
    clean = []

    for paragraph_tag in paragraph_tags:

        paragraph_text = paragraph_tag.get_text()
        clean.append(paragraph_text)
        #print(paragraph_text)

    

    full_text = ""
    with open("pagecontent.txt", "w") as f:
        for sen in clean:
            f.write(sen + "\n")
            full_text += sen
    # for sen in clean:
    #     full_text += sen
    return full_text

#print(extract_content("https://www.msn.com/en-us/money/companies/ericsson-partners-with-canadian-government-to-invest-ca-470m-in-r-d-sites/ar-AA19Yh5q"))
#print(extract_content("https://infotel.ca/newsitem/hkn-jets-golden-knights/cp868188782"))