import requests
import json
from read_content import extract_content
import os
#import word_sum_t5
import word_sum_pegasus
import textrank4keyword
import t5_word_sum
import yaml
import wordsum_gpt

#Proccess: Connect to the Bing API to pull data -> apply the summarization models

# Define your Bing News Search API endpoint and key
subscription_key = "**********************" 
search_url = "https://api.bing.microsoft.com/v7.0/news/search"

# Define a function to search for news articles based on a given topic
def search_news(topic, max_articles):
    #TODO: need to delete all content.txt after start (done)
    files = os.listdir("storage")
    for file in files:
        if file.startswith('content'):
            os.remove("storage/"+file)
    
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {
        "q": topic,
        #"category": "Entertainment",
        "count": max_articles,
        "freshness": "Day",
        "mkt": "en-CA",
        "sortBy": "Date"
    }

    response = requests.get(search_url, headers=headers, params=params)
    response_json = json.loads(response.content.decode("utf-8"))

    
    # for article in response_json["webPage"["value"]]:
    #     articles.append({
    #         "title": article["name"],
    #         "description": article["description"],
    #         "url": article["url"],
    #         "source": article["provider"][0]["name"],
    #         "published": article["datePublished"]
    #     })
    data = response_json
    #print(data)
    #This can be used for bing search api, can be develop to image search, video search in the future...
    #urls = [item['url'] for item in data['webPages']['value']]

    #extract url, title, and description
    
    
    urls = [item['url'] for item in data['value']]
    titles = [item['name'] for item in data['value']]
    descriptions = [item['description'] for item in data['value']]
    return urls, titles, descriptions

def main_extraction_to_file(topic, max_articles = 5, num_keyword = 5):
    # Example usage
    urls,titles, descriptions = search_news(topic, max_articles)
    list_of_contents = []
    # print(urls)
    # for url in urls:
    #     #print("11111")
    #     list_of_contents.append(extract_content(url))
    #     print(url)
    
    for i in range(len(urls)):
        list_of_contents.append(extract_content(urls[i]))
        #print(urls[i], titles[i], descriptions[i])
    
    for i in range(len(urls)):
        with open("storage/content"+str(i)+".txt", "w") as f:
            f.write("URL: %s \n"%(urls[i]))
            f.write("TITLE: " + titles[i] + "\n")
            f.write("DESCRIPTION: " + descriptions[i] + "\n")
            #handle the case that it returns none
            try:
                f.write(list_of_contents[i])
            except TypeError:
                continue
        with open('disabled_content_list.yaml', 'r') as f:
            classes = yaml.full_load(f)
            disabled_str = classes['disabled']
            #print(disabled_str)
        switch = True
        for s in disabled_str:
            if s in list_of_contents[i]:
                switch = False
        #if not("Please enable JS and disable any ad blocker" in list_of_contents[i] or list_of_contents[i] == "" or "This website is using a security service to protect itself from online attacks. The action you just performed triggered the security solution." in list_of_contents[i]):# or "/video" not in urls[i]:
        if switch:
            print(urls[i])
            #print("This is summary: \n", word_sum_t5.word_sum(list_of_contents[i]))
            print("This is summary: \n", t5_word_sum.word_sum_t5(list_of_contents[i]))
            pegasus = word_sum_pegasus.pegasus_sum(list_of_contents[i])
            if pegasus != "All images are copyrighted.":
                print("This is pegasus summary: \n", pegasus)
            gpt = wordsum_gpt.summarize(list_of_contents[i])
            if gpt != None:
                print("This is gpt summary: \n", gpt)
            print("This is top %s keyword(s)"%(str(num_keyword)), textrank4keyword.extract_keyword(list_of_contents[i], num_keyword))
        


    
#main_extraction_to_file("Canada Education", 3, 5)
##useful link:
#https://levelup.gitconnected.com/api-tutorial-how-to-use-bing-web-search-api-in-python-4165d5592a7e

#TODO: save credentials APIs to yaml encrypted file
#TODO: handle some exception when requests.get fail...
#TODO: What to do with titles, description. Maybe extract author...
#TODO: handle the case that 3 page found but 4 is inputted in count. Maybe just need to explain in the description that the maximum only (maybe lesser)
#TODO: Handle the case that we can't access to the page (maybe it block the web scrapper)
#TODO: video or images news?
#TODO: Test TFIDF sumarization model