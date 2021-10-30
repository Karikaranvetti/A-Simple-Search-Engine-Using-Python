import sys   # for command line aregument 
import os  # for store the file 
import requests  #for http requsts 
from bs4 import BeautifulSoup   # for graping the web page components

topic={}   # for storing the full new headlines 
SITE='https://lite.cnn.io/'    # the news website end point 
source=requests.get(SITE).text   # geting the response as text 

suop = BeautifulSoup(source,'html.parser')  # extracte the data from response using bs4 
for heading in suop.find_all('li'): # the website all hedlines are in li tag so grap all li tags 
    heading_text=heading.text      #loop through geting all hedline name 
    try:         # and trying to get the link for that heading 
        link='https://lite.cnn.com'+heading.a['href']    #make the link 
    except Exception as e:     # if the link is not exist then make the link as none 
        link=None
    topic[heading_text]=link    # storing the heading and currosponding link 
    
keywords = sys.argv[1:]     # geting the keyword for shearching from   commandline arguments 
keys = []  # for strore the all matching headlines 
for key in topic.keys():    #loop Throgh all headlines 
    for word in key.split(' '):     # splite the heading with space and make that as word 
        for keyword in keywords:    # and loop throgh the all keywords 
            if keyword.lower()==word.lower():     # if the keyword and word is match then we taking that corrsponding headline 
                keys.append(key) #strore in list 
if os.path.exists("SelectedNews.html"):     # if the file already exist then delete it 
    os.remove("SelectedNews.html") 
f = open("SelectedNews.html", "a")    # then create a file with appending mode 
for subtopic in keys:  # then loop throgh the selected headlins 
    source1=requests.get(topic[subtopic]).text   # geting the respons for specific headline 
    suop1 = BeautifulSoup(source1,'lxml')  # geting the web componets 
    try:     # try to get the update time 
        updateTime=suop1.find('div',class_='afe4286c').div   # geting the updated time 
    except Exception as e:  # the componet not exist then 
        updateTime=None   # make the update time as none 
    
    # print(updateTime)    
    # print(topic[subtopic])
    f.write("     \n")  
    f.write(str(updateTime))  # first write the news update time 
    f.write("     \n")
   
    try:    # then try to get the heading of the news 
        head=suop1.find('div',class_='afe4286c').h2    # geting the news 
    except Exception as e:   # if not exist then 
        head=None    # make that as none
    # print(head.text)
    f.write(str(head))  # write the heading into file 
    f.write("    \n")
    for sub_detils in suop1.find_all('p'):    # for geting the detiles for the news first we get the all p tag 
                                                #and loop throuh it 
        # print(sub_detils.text)
        f.write(str(sub_detils))   # writing the detile paragraph by pragraph 
        f.write("    \n")
    
f.close()    # finaly close the file 
print('Successfully data fatch from "https://lite.cnn.io/" and stored in "SelectedNews.html" ')