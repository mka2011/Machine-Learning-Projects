#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 15:50:29 2020

@author: manavagrawal
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 18:48:48 2020

@author: manavagrawal
"""

import urllib.request
import urllib.parse
import requests
import re
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import csv

listOfCountries = ["switzerland","canada","japan","germany","australia","united%2Bkingdom","united%2Bstates","sweden","netherland","norway","india","uae","oman","qatar","new%2Bzealand","denmark","finland","china","singapore","spain","italy","malaysia","poland","indonesia"]
hotelLinks = []




for i in listOfCountries:
    url = "https://www.booking.com/searchresults.en-gb.html?ss="
    url = url+i
    print("Country Visit : ",i)
    result = requests.get(url)
    
    parsedTags = BeautifulSoup(result.text,"html.parser")
                
    HotelNames = parsedTags.findAll("a",{"class" : "bui-card__header_full_link_wrap"})
    vis = {}
    
    for j in HotelNames:
        hotelLinks.append(j)        
        

print("Scraping Hotels")
with open('hotels2.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name Of Hotel','City','Country','Rating','Amenities','Description','Reviews'])

    for i in hotelLinks:
        hotelDetails = []
        hotelDetails.append(i.get("title"))
        print(hotelDetails[0])
        
        url2 = "http://www.booking.com" + i.get("href")
        result2 = requests.get(url2)
        parsedTags2 = BeautifulSoup(result2.text,"html.parser")
        
        parseAddress = parsedTags2.findAll("span",{"class" : "hp_address_subtitle js-hp_address_subtitle jq_tooltip"})
        s = str(parseAddress[0])
        s2 = s.split()
        l = len(s2)
        city = s2[l-3]
        city = city[:-1]
        country = s2[l-2]
        hotelDetails.append(city)
        hotelDetails.append(country)
        
        parseRating = parsedTags2.findAll("div",{"class":"bui-review-score__badge"})
        hotelDetails.append(parseRating[0].text)
        
        parseFacility = parsedTags2.findAll("div", {"class" : "important_facility"})
        nosOfFac = len(parseFacility)//2
        strFac = ""
        for k in parseFacility:
            if nosOfFac == 0:
                break
            nosOfFac = nosOfFac-1
            strFac = strFac + ", " + k.text[2:-1]
            
        strFac = strFac[2:]
        hotelDetails.append(strFac)
                
        parseDesc = parsedTags2.find("div", {"id" : "property_description_content"}).find("p")
        tempList = parseDesc.contents
        strPropDesc = ""
        for k in tempList:
            if type(k) == NavigableString:
                strPropDesc = str(k)
                break
        hotelDetails.append(strPropDesc)
                
        parseReviews = parsedTags2.findAll("span",{"class":"c-review__body"})
        counter = 0
        reviewsOfHotel2 = ""
        for k in parseReviews:
            if counter == 2 :
                break
            reviewsOfHotel2 = reviewsOfHotel2 + (k.text) +"\n"
            counter = counter + 1
        hotelDetails.append(reviewsOfHotel2)
    
        writer.writerow(hotelDetails)




