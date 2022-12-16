# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 14:54:29 2022

@author: hbora

@Title : SI507 Final Project - main

@Description: This script has the function which calls the GUI scripts to get
 user input. Once user input is taken, the tree data structure is created. We 
 then query this tree for our required values. We get the final list of 
 listings which is cleaned up a little and returned.

"""
import json
import create_tree as Tree
from input_ui import get_user_input
from get_user_coords import get_coords

def get_res():
    """
    Summary
    -------
    Gets user input, creates tree, query tree and return results
    
    Description
    -------
    This function first reads the cache data from the stored json file.
    Then call script which gets user location as (lat,long) tuple
    Further call the script which gets user choice of dist, price and rating 
    preference as (dist,price,rating) tuple with values between (0,0,0)-(3,3,3)
    Create tree data structure object with user location
    Load cached data into tree data structure
    Query tree for user prefernce and get output of listings. Put listing data 
    into cleaner json for display
    
    Returns
    -------
    html_json : list of dictionaries containing restaurant data
    """
    

    with open('cache_data.json', 'r') as f:
        cache_data = json.load(f)

    
    user_loc = get_coords()
    
    query = get_user_input()
    
    tree = Tree.root(user_loc)   
    
    for listing in cache_data:
        tree.insertlisting(listing)
    
    #tree.printTree()
    
    results = tree.queryDist(query)
    
    html_json = []
    for res in results:
        html_dict = {"Name":res["name"],
                     "Description":res["desc"],
                     "Rating":res["rating"],
                     "Price level":"$"*res["price_level"],
                     "Dist from you":"{}km".format(res["dist"])}
        html_json.append(html_dict)
        
    return html_json
    
    
if __name__ == "__main__":
    get_res()