import requests as req
from bs4 import BeautifulSoup
import random
import time


#url:= url of file movie_i that contains the usrls of wikipedia
#path:= path of folder where save the pages of wikipedia; with / or \ at the end
def crawl(url, path):
    if type(path)!=str:
        raise Exception('input path must be a string! Not a {}'.format(type(path)))
    request=req.get(url)
    soup=BeautifulSoup(request.text, 'html.parser')
    ftableS=str(soup.find_all('table'))
    table=BeautifulSoup(ftableS, 'html.parser')
    urls=table.find_all('a')

    i=0
    for link in urls:
        with open(''.join([path, 'article_', str(i), '.html']), 'w') as f:
            try:
                text=req.get(link.get('href')).text
            except:
                time.sleep(20*60)
                text=req.get(link.get('href')).text
            f.write(text)
        time.sleep(random.randrange(1, 5))
        i+=1
    print('finish crwaling')
