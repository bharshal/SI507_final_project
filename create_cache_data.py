# -*- coding: utf-8 -*-
"""
@author: hbora, 23841636

@Title : SI507 Final Project - Create cached data

@Description: Query Google places API for restaurants listing in Ann Arbor by 
lat-long cordinates, keep only the unique values, then query the detailed API 
for more information ion those listings, keep relevant information, discard the
rest and save data as cache in json format.
"""

import sys

#sys.path.append("C:/Users/hbora/Downloads/SI_507/final_project/code/")

import re
import requests
import json

# # four co-ords for annarbor border: topleft, topright, bottomleft, bottomright
# tl = (42.31672728454659, -83.80731873113874)
# tr = (42.31672728454659, -83.67290787670282)
# bl = (42.23823420163313, -83.80731873113874)
# br = (42.23823420163313, -83.67290787670282)

# # horizontal and vertical separation of the borders
# horz_dist = tr[1] - tl[1]
# vert_dist = tr[0] - br[0]

# # divide the quadrilateral into 10x10 grid of co-ordinates

# cords_list =[]
# #horz loop
# for i in range(10):
#     # vert loop
#     for j in range(10):
#         long = tl[1] + (horz_dist/10)*i
#         lat = tl[0] - (vert_dist/10)*j
#         coord = (lat,long)
#         cords_list.append(coord)
        

# # query the places api for restaurant listings in grid
# total_data = {"results":[]}
# for cord in cords_list:

#     url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius=750&type=restaurant&key=AIzaSyAO6eiPgJ5nvslGJcv8fQ9wfE5qrvEg-Uo".format(cord[0],cord[1])
#     payload={}
#     headers = {}
    
#     response = requests.request("GET", url, headers=headers, data=payload)
    
#     resp_json = json.loads(response.text)
#     total_data["results"] += resp_json["results"]
    
# # save the raw data (at this point the data has duplicate results because)    
# with open('complete_raw_data.json', 'w') as f:
#     json.dump(total_data, f)
    
##############################################################################

#                           2nd part                                        #

##############################################################################

# list of common words that are to be filtered 
filter_words = ['isn', 'mightn','into', 'doesn', 'above', "you'll", 'no', "wouldn't", 'now', 'an', "hasn't", 
'during', 's', 'there', "hadn't", 'at', "doesn't", 'yourselves', 'do', 'will', 'ain', 'myself', 'or', 
'too', 'itself', 'does', 'in', 'under', 're', 'hadn', "isn't", 'mustn', 'ourselves', 'where', 'nor', 
'further', 'such', 'can', 'am', 'were', 'has', 'weren', "needn't", 'yourself', 'theirs', "don't", 'our',
'through', 't', 'its', 'm', 'so', 'any', 'll', 'most', 'herself', 'more', 'against', 'me', 'being', 
'wasn', 'both', 'won', 'd', 'couldn', 'himself', 'with', 'from', 'needn', 'down', 'your', 'on', 'few', 
'that', 'are', 'until', 'my', 'y', 'ours', "mightn't", 'yours', 'aren', 'other', 'because', 'if', 'below', 
'why', "didn't", "that'll", 'have', 'not', 'haven', 'off', 'but', 'own', 'she', 'which', 'ma', 'him', 'here', 
'he', 'when', 'for', 'is', 'just', 'hasn', 'these', 'as', 'doing', 'to', 'after', 'of', 'o', 'some', "aren't",
"it's", 'up', 'be', 'before', 'we', 'their', 'his', 'then', 'should', 'been', 'the', 'you', 'all', 'don',
"shouldn't", "wasn't", "shan't", 'only', "you've", "couldn't", 'very', 'did', 'her', 'each', 'while', 'than',
'how', 'this', 'who', 'it', 'wouldn', "you're", 'those', 'they', 'again', 'by', 'what', 'hers', 'a', 
"haven't", 'had', 'about', 'shan', 'was', 'themselves', 'once', 'same', 've', 'between', "won't", 'and',
"you'd", "mustn't", 'having', "should've", 'out', 'didn', 'shouldn', 'i', 'them', 'over', "weren't", 
'whom', "she's", 'also', 'th', 'ive','food']

# function to clean review data and remove filter words
def word_process(review_text):
    mod_str = re.sub('[^A-Za-z ]+', '', review_text).split()
    mod_str = [i for i in mod_str if i not in filter_words]
    mod_str = set(mod_str)
    return mod_str


# function to query Places Details API for reviews and working hours using 
# placeid
def get_reviews_hours(place_id, name):
    url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=editorial_summary,reviews,opening_hours&key=AIzaSyAO6eiPgJ5nvslGJcv8fQ9wfE5qrvEg-Uo".format(place_id)
    
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    resp_json = json.loads(response.text)
    
    open_hours = []
    try:
        open_hours = resp_json["result"]["opening_hours"]["periods"]
    except:
        pass
    
    try: 
        desc = resp_json["result"]["editorial_summary"]["overview"]
    except: 
        desc = ""
        
    try: 
        reviews = resp_json["result"]["reviews"]
    except: 
        return open_hours,[],desc
    

    
    comb_text = name.strip().lower()
    for review in reviews:
        comb_text += review["text"].strip().lower()
        comb_text += " "
    review_keywords = word_process(comb_text)
    return open_hours, list(review_keywords), desc
    
    
# read previously stored raw data
with open('complete_raw_data.json', 'r') as f:
    json_data = json.load(f)

# keep only unique listings using Set, delete irrelevant info and add review 
# data to dictionary using function above
seen = set()
uniq = []
for x in json_data["results"]:
    if x["name"] not in seen:
        x["location"] = x["geometry"]["location"]
        del x["geometry"]
        try:
            del x["opening_hours"]
        except: pass
        del x["business_status"]
        del x["icon"]
        del x["icon_background_color"]
        del x["icon_mask_base_uri"]
        del x["reference"]
        del x["scope"]
        try:
            del x["photos"]
        except: pass
        del x["plus_code"]
        del x["vicinity"]
        
        x["open_hours"], x["keywords"], x["desc"] = get_reviews_hours(x["place_id"],x["name"])
        del x["place_id"]
        
        uniq.append(x)
        seen.add(x["name"])


# save final data as cache
with open('cache_data.json', 'w') as f:
    json.dump(uniq, f)