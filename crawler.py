import re
import requests
import sys
import time
from bs4 import BeautifulSoup as soup


def compose_url(postID,year,month,day,hour,min,sec):
    return 'https://www.cnblogs.com/post/prevnext?postId={0}&blogId=267676&dateCreated={1}%2F{2}%2F{3}+{4}%3A{5}%3A{6}&postType=1'.format(postID,year,month,day,hour,min,sec)

def get_page_info(url):
    postID = url.split("/")[-1].split(".")[0]
    result = requests.get(url)
    page = result.text
    doc = soup(page,'html.parser')
    title_line = doc.select("#cb_post_title_url")[0]
    # print(type(title_line))
    href = title_line.get('href')
    title = title_line.get_text()
    timestr = doc.find_all('script')[6].text.split(",")[5].split(";")[0].split("=")[1]
    m=re.match(r'\'(\d+)\/(\d+)\/(\d+) (\d+)\:(\d+)\:(\d+)\'',timestr)
    y,m,d,h,i,s = m.group(1,2,3,4,5,6)
    query_url = compose_url(postID,y,m,d,h,i,s)
    return title,href,query_url




def get_next_page_url(url):
    result = requests.get(url)
    page = result.text
    doc = soup(page,'html.parser')
    next_tag = doc.find_all('a')[-1]
    href = next_tag.get('href')
    
    return href

def printHtml(blogs):
    with open('OpenStack.html','w',encoding='utf-8') as f:
        f.write('<!DOCTYPE html>')

        f.write('<html>')
        f.write('<meta charset="utf-8"/>')

        f.write('<head>')
        f.write('<title>每天5分钟玩转 OpenStack</title>')
        f.write('</head>')
        f.write('<body>')
        for i,item in enumerate(blogs):
            (href,title)=item
            f.write('<p><a href="{0}" target="_BLANK">({1}).{2}</a></p>'.format(href,i+1,title))
        f.write('</body>')
        f.write('</html>')

# python .\crawler.py https://www.cnblogs.com/CloudMan6/p/5224114.html
if __name__ == '__main__':
    blogs=[]
    url = sys.argv[1]
    for i in range(1,176):
        title,href,query_url = get_page_info(url)
        url = get_next_page_url(query_url)
        blogs.append((href,title))
   
    printHtml(blogs)

        
    

