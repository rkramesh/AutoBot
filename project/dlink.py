import config
import os,sys,platform
import wget,re
import logging
import requests,urllib2,bs4

requests.packages.urllib3.disable_warnings()


class downloadlink(object):
     def __init__(self, msgText,osType):
         self.msgText = msgText
         self.osType = osType


     def dlink1(self,msgText):
        if platform.system().lower() == 'windows':
            wget.download(self.msgText)

     def gsearch(self,query):
            DIR=config.media_storage_path#downloads the images in the current directory"
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
                fdata = open(DIR+'/'+query+".jpg", 'wb')
                fdata.write(raw_img)
                fdata.close()
                print 'Done!'
                return (query+".jpg")
            else:
                print 'No Image'
     def amazon(self,query):
        url = 'http://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias' \
          '%3Daps&field-keywords={}'.format(query.replace(' ', '+'))
        
        response = requests.get(url,
                                headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                       '6.2; WOW64) AppleWebKit/'
                                                       '537.36 (KHTML, like '
                                                       'Gecko) Chrome/37.0.2062.'
                                                       '120 Safari/537.36'})
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        #print response.content
        prod_list = []
        prod_req =[]
        prods = {}
        asins_dict = {}
        asins_sponsored_dict = {}
        for tag in soup.find_all('li', {'class': 's-result-item'}):
           
            f = open(config.amz_temp, "a")
            asins_dict[tag.get('data-asin')] = tag.get('id')
            product = prods['Product'] = tag.find('h2').text.encode('ascii','ignore')
            by_list = tag.find_all('span',
                                   {'class': 'a-size-small '
                                             'a-color-secondary'})
            
            #print by_list
            if len(by_list) > 0:
                if 'by ' in by_list[0].string:
                    prods['Seller'] = by_list[1].string.encode('utf-8')
                else:
                    prods['Seller'] = ' '
            
            try:
               price_list = tag.find('span',
                                      {'class': 'a-size-base '
                                                'a-color-price '
                                                's-price a-text-bold'}).text
            except AttributeError:
                   price_list = 'Price Not Found'
            #print price_list
            if len(price_list) > 0:
                price_list = prods['Price'] = price_list.encode('ascii','ignore')
            
                
            prod_list.append(prods.copy())
            f.write(product+' :₹ '+price_list+"\n")
                 

        with open(config.amz_temp, 'r') as myfile:
             data=myfile.read()
        
        return data
        
        #return prods['Product'],

      
  
