# -*- coding: utf-8 -*-
import sys
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import json

reload(sys)
sys.setdefaultencoding('utf-8')

url = "http://www.imdb.com/title/tt1798709/?ref_=fn_al_tt_1"
###test another url###
#url = "http://www.imdb.com/title/tt0388125/?ref_=fn_al_tt_4"
res = urllib2.urlopen(url)
html = res.read()
sp = BeautifulSoup(html)


###find movie_name###
movie_name = sp.title.string
#print movie_name,"\n"

###find date###
date = sp.find_all('a',{'title':'See all release dates'})
#print date[0].get_text().replace("\n",""),"\n"

###find movie_genre###
movie_genre = sp.find_all('div',{'itemprop':'genre'})
#print movie_genre[0].get_text().replace("\n",""),"\n"

###find keywords###
keywords = sp.find_all('div',{'itemprop':'keywords'})
#print keywords[0].get_text().replace("\n","").replace("| See more »",""),"\n"

###find director###
director = sp.find_all('div',{'itemprop':'director'})
#print director[0].get_text().replace("\n",""),"\n"

###find writer###
writer = sp.find_all('div',{'itemprop':'creator'})
#print writer[0].get_text().replace("\n",""),"\n"

###find rating###
rating = sp.find_all('div',{'class': 'titlePageSprite star-box-giga-star'})
#print rating[0].get_text().replace("\n",""),"\n"

#movie description
description = sp.find_all('div',{'itemprop':'description'})
#print description[0].get_text().replace("\n",""),"\n"


###fing cast###
cast_tables = pd.read_html(html)
cast_table = cast_tables[1][1]
#cast name is range 1 to len(cast_list) 
cast_list = list()
for i in range(1,len(cast_table)):
	cast_list.append(str(cast_table[i]))

#print cast_list

json_data = {
	"movie_title": movie_name,
	"movie_date": date[0].get_text().replace("\n",""),
	"movie_genre": movie_genre[0].get_text().replace("\n","").replace("\xc2\xa0","").split("Genres: ",1)[1],
	"movie_keywords":keywords[0].get_text().replace("\n","").replace("| See more »","").split("Keywords: ",1)[1],
	"movie_direcotr":director[0].get_text().replace("\n",""),
	"movie_writer":writer[0].get_text().replace("\n",""),
	"movie_rating":rating[0].get_text().replace("\n",""),
	"movie_description":description[0].get_text().replace("\n","").split("Written",1)[0],
	"movie_cast":[dict(name=nm) for nm in cast_list]
}

	
f = open('movie_json','w')
f.write(json.dumps(json_data))
f.close()



