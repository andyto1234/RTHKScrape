import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import progressbar
import urllib.request
import multiprocessing as mp
import os
import pathlib




pbar = None


def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


year_string='2015-2016'
pathlib.Path(year_string).mkdir(parents=True, exist_ok=True)

# os.mkdir(year_string, exist_ok=True)
directory = 'https://app3.rthk.hk/special/awardpro/award15/'
website = requests.get(directory)
soup = BeautifulSoup(website.content, 'html.parser')
# id_1 = soup.find(class_ = "rollover2")
# id_2 = soup.find(class_ = "rollover3")
# print(id.text)

links = soup.find_all(href=True)
list_link=[]
for el in links:
    holder = el['href']
    if holder[0]=='t':
        list_link.append(holder)
        print(holder, len(list_link))

failed_list=[]
print(len(list_link))

def scrape(k):
#     driver = webdriver.Chrome(executable_path = chromepath)
#     driver.get(directory+link)

#     html = driver.page_source
#     soup = BeautifulSoup(html)

    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                'Accept-Language': 'en-US, en;q=0.5'})

    website_sub = requests.get(directory+list_link[k], headers=HEADERS)
    soup = BeautifulSoup(website_sub.content, "html.parser")
#     body = soup.find_all('body')
#     print(body)
    dom = etree.HTML(str(soup))
    string = dom.xpath('/html/head/script[10]/text()')[0]

    results = re.findall('file: "(.*?)"', str(string))
    print(string,results)
    title = soup.find('div', class_='prog_title')
    title =  title.text.replace('	',"")
    title =  title.replace('  ',"")
    print(directory+list_link[k], results, title)
    counter=0
    for result in results:
        if result != 'https://app3.rthk.hk/mp4':
            urllib.request.urlretrieve(result, year_string+'/'+title+'.mp4', show_progress) 
            counter+1
        else:
            failed_list.append(directory+list_link[k])
            f=open(year_string+'/failed','w')
            f.write(str(title)+"\n"+str(result)+"\n"+"\n")
            f.close()

            
pool = mp.Pool(processes=32)

mylist = [y for y,x in enumerate(list_link)]
# print(mylist)
pool.map(scrape, mylist)

print(failed_list)