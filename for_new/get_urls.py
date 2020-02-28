from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import random
import os
import re
import argparse

def get_youtube_urls(scroll_times, maximun_play_time):
    emoji_pattern = re.compile("["
       u"\U0001F600-\U0001F64F"  # emoticons
       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
       u"\U0001F680-\U0001F6FF"  # transport & map symbols
       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
       u"\U0001f923"
       u"\u2022"
       u"\uD83C-\uDBFF"
       u"\uDC00-\uDFFF"
                          "]+", flags=re.UNICODE)


    driver = webdriver.Chrome(os.path.join(os.getcwd()+"\\for_new\\ch", 'chromedriver.exe'))

    search_words = open('youtube_search_words.txt').read().splitlines()

    new_urls_file = open(os.path.join("for_new\\txts\\urls", "new_urls.txt"), 'a')

    for search_word in search_words:
        driver.get('https://www.youtube.com/')

        driver.find_element_by_name("search_query").send_keys(search_word + "\n")

        body = driver.find_element_by_tag_name('body')#스크롤하기 위해 소스 추출
        
        
        num_of_pagedowns = scroll_times
        #10번 밑으로 내리는 것
        while num_of_pagedowns:
            time.sleep(2)
            body.send_keys(Keys.PAGE_DOWN)
            num_of_pagedowns -= 1
        time.sleep(2)

        html0 = driver.page_source

        html = BeautifulSoup(html0,'html.parser')
        video_ls=html.find_all("ytd-video-renderer", class_ = 'style-scope ytd-item-section-renderer')

        tester_url = []
        for i in range(len(video_ls)):
            running_time = str(video_ls[i].find("span", class_='style-scope ytd-thumbnail-overlay-time-status-renderer').text)
            splitted_time = running_time.split(":")

            play_time_minites = 0

            if len(splitted_time) >= 3:
                play_time_minites = int(splitted_time[0]) * 60 + int(splitted_time[1])
            else:
                play_time_minites = int(splitted_time[0])


            if play_time_minites <= maximun_play_time:
                url = "https://www.youtube.com/" + str(video_ls[i].find('a', id ='thumbnail')['href'])
                tester_url.append(url)


        for new_urls in tester_url:
            new_urls_file.write(new_urls + '\n')
    
    new_urls_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'parser for preproccess')
    parser.add_argument(
        "--scroll_times",
        type=int,
        )

    parser.add_argument(
        "--maximum_play_time",
        type=int,
        )

    args = parser.parse_args()

    get_youtube_urls(args.scroll_times, args.maximum_play_time)