#!/usr/bin/python
import bs4 
import re
import os
import requests
import urllib2

requests.packages.urllib3.disable_warnings()

def search(query):
    DIR="." #downloads the images in the current directory"
    img_name = query
    
    url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
    

    header = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url,verify=False,
                                headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                       '6.2; WOW64) AppleWebKit/'
                                                       '537.36 (KHTML, like '
                                                       'Gecko) Chrome/37.0.2062.'
                                                       '120 Safari/537.36'})
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    images=soup.find('img', {'src': re.compile('gstatic.com')})
    
    if images:
        raw_img = urllib2.urlopen(images['src']).read()
        fdata = open(query+".jpg", 'wb')
        fdata.write(raw_img)
        fdata.close()
        print 'Done!'
        return (query+".jpg")
    else:
        print 'No Image'
       
    
  
if __name__ == "__main__":
    query = input("Enter your search Query?  eg: 'Dolphin' ")#provide the query within quotes
    product_list = search(query)
        
