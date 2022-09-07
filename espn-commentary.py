#download all the commentary text by simulating the page scrolling using selenium!

import time
from selenium import webdriver
from bs4 import BeautifulSoup

import urllib.request
import pandas as pd

l="https://www.espncricinfo.com/series/south-africa-in-england-2022-1276896/england-vs-south-africa-3rd-t20i-1276915/ball-by-ball-commentary"

#l = "https://www.espncricinfo.com/series/new-zealand-in-scotland-2022-1311224/scotland-vs-new-zealand-only-odi-1307479/ball-by-ball-commentary"

driver = webdriver.Chrome(executable_path="/home/dhiraj/chromedriver")

driver.get(l) 
scroll_pause_time = 5 # wait time in seconds before scrolling
screen_height = driver.execute_script("return window.screen.height;")

i = 1

#loop until there is no more scrolling to do
while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)

    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        print("Total scrolls: ",i)
        break

sp = BeautifulSoup(driver.page_source, "html5lib")

c='ds-text-tight-m ds-font-regular ds-flex ds-px-3 ds-py-2 lg:ds-px-4 lg:ds-py-[10px] ds-items-baseline lg:ds-items-center ds-relative'
divs = sp.find_all("div",c) # this is where the commentary is


over, outcome, short_desc, detail_desc = [],[],[],[]

for i in range(len(divs)):
	div = divs[i]
	a = div.get_text(separator="\t").split("\t")
	#print(a)
	detail_desc.append(a)

#	detail_desc.append(div.text)
#	print(div.text)
#	print("---")
	spans = div.find_all("span")
	# for j in range(len(spans)):
	# 	print(spans[j].text)
	# print("***")	
	over.append(spans[0].text)

	if spans[1].text not in ['1','2','3','4','W']:
		outcome.append('0')
	else:
		outcome.append(spans[1].text)
	
	short_desc.append(spans[2].text)


# to spam on twitter
def create_msg(detail_desc):
	msg = []
	for i in range(len(detail_desc)):
		s = detail_desc[i][0]
		for j in range(1,len(detail_desc[i])):
			s+= " " + detail_desc[i][j]
		msg.append(s)
	return msg


over_list, outcome_list, who2who_list, short_desc_list, detail_desc_list = [],[],[],[],[]
bowler, batter = [],[]

for a in detail_desc:
    #print("Over \t Outcome \t Who2Who \t bowler \t batter \t Short_description \t Description")
	#print(a[0],"\t", a[1], "\t", a[2] ,"\t", a[2].split(" to ")[0], "\t", a[2].split(" to ")[1], "\t", a[3], "\t",a[4:len(a)])
    over_list.append(a[0])
    outcome_list.append(a[1])
    who2who_list.append(a[2])
    bowler.append(a[2].split(" to ")[0])
    batter.append(a[2].split(" to ")[1].replace(",","").rstrip())
    short_desc_list.append(a[3])
    detail_desc_list.append(a[4:len(a)])

data = {'overs':over_list, 'outcomes':outcome_list, 'who2who':who2who_list, 'bowler': bowler, 'batter':batter,
 'short_desc':short_desc_list, 'detail_desc':detail_desc_list}

df = pd.DataFrame(data=data)
df['detail_desc'] = df['detail_desc'].apply(lambda x: x.replace("['","")).apply(lambda x: x.replace("']",""))

# df['detail_desc'].apply(func=len) # gives length of each detail_desc entries
# max(df['detail_desc'].apply(func=len)) # gives longest detail_desc entry


# longest_desc = df['detail_desc'].apply(func=len).idxmax(axis=0) # get the index of longest description
# '''
