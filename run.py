import hashlib
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time


class VbullettinFetcher:
    
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()

    def doLogin(self):
        r = self.session.post(self.base_url + 'login.php?do=login', {
            'vb_login_username': self.username,
            'vb_login_password': self.password,
            'vb_login_md5password': hashlib.md5(self.password.encode()).hexdigest(),
            'vb_login_md5password_utf': hashlib.md5(self.password.encode("utf-8")).hexdigest(),
            'cookieuser': 1,
            'do': 'login',
            's': '',
            'securitytoken': 'guest'
        })

    def get(self, url):
        return self.session.get(url)
    
    def extractThreads(self, page_html):
        soup = BeautifulSoup(base_page.content, 'lxml')
        return soup.find_all('a', id=re.compile("thread_title_[6789]"))
    
    def extractAllLinksFromThreads(self, threads, delay_between_requests = 1):
        result = []
        for thread in threads:
            full_url = self.base_url + thread.get('href')
            thread_title = thread.getText()
            links = self.__extractAllLinksFromThread(full_url)
            result.append({"links" : links, "title" : thread_title, "url" : full_url})
            time.sleep( delay_between_requests )
        return result
    
    def __extractAllLinksFromThread(self, full_url):
        result = []
        posts = self.__postsFromThread(full_url)
        for post in posts:
            links = self.__extractAllLinksFromPost(post)
            for link in links:
                result.append(link.get('href'))
        return result
        
    def __postsFromThread(self, full_url):
        thread_page = self.get(full_url)
        thread_page_soup = BeautifulSoup(thread_page.content, 'lxml')
        p = thread_page_soup.find("div", {"id": "posts"})
        if p is not None:
            return p.findChildren("div" , recursive=False)
        return []

    def __extractAllLinksFromPost(self ,post):
        message_container = post.find('td', id=re.compile("td_post"))
        if message_container is not None:
            return message_container.find_all('a')
        return []
    

