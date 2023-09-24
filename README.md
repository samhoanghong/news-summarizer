# news-summarizer

## Purpose: 

Welcome to the News Summarization Project. This project aims to provide a tool for summarizing news articles quickly and effectively. In the age of information overload, news summarization can be a valuable asset for staying informed without spending excessive time reading lengthy articles.

This documentation will guide you through the project's overview, how to get started, usage instructions, key features, and the dependencies required for running the project.

## Overview:

The primary goal of this project is to develop a Python-based news summarization tool that can:

- Automatically extract important information from news articles.
- Generate concise and coherent summaries of news articles.
- Save users time by providing a brief overview of news stories.

Key Features:

- Text Summarization: The project employs natural language processing techniques to extract and summarize the main points of news articles.
- Web Scraping: It can scrape news articles from various news websites and summarize them.
- User Interface: A user-friendly command-line interface (CLI) or web-based interface for easy interaction.

## Pipeline:

- In the main.py, users input topic, number of articles to generate, number of keywords

- The program will connect to Bing Search API to collect the URLs, Title, Author, Data, etc.

- It will save all information in a folder called storage. URL, TITLE, DESCRIPTION, BODY of NEWS

- In terms of BODY of NEWS, this program will perform web-scrapping to extract the main content of it. Firstly, the program will use CURL to pull the content. Secondly, it uses beautifulSoup, and exclude tags (TITLE, FOOTER, ADs, etc.) to extract only main body of it (It will be continuely updated). Please have a look at read_content.py and exclude_config.yaml for more information.

- Then, it will apply different techniques to summarize news (currently testing on different models such as T5, pegasus, OpenAI, TFIDF.

- It will also apply textrank algorithm to extract keywords.

## Next steps:

- Refactoring codes
- Adding security layers to save credentials
- Updating Documentation
- Developing front-end to improve UI-UX (also have a draft of streamlit)
- Fine-tuning, training models for more accuracy uses
- Updating the exclude tags for better body news
- Handling errors

