# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 16:21:55 2022

@author: hbora

@Description: Creates tree data structure. Can be run independently by 
directly running file with sample json. (Already setup in __main__)
"""
from lat_long_dist import distance

class root:
    """Root of restaurants tree
    """
    def __init__(self, user_loc):
        """Creates three distance children each denoting one of the distance 
        buckets. The buckets are as follows - 
            * 0 to 2km: Dist1
            * 2km to 4km: Dist2
            * 4km to 8km: Dist3
        """
        self.dist1 = Dist("Dist1")
        self.dist2 = Dist("Dist2")
        self.dist3 = Dist("Dist3")
        self.user_loc = user_loc
    
    def insertlisting(self, data):
        res_loc_lat = float(data["location"]["lat"])
        res_loc_long = float(data["location"]["lng"])
        dist = distance(self.user_loc[0],res_loc_lat,self.user_loc[1],res_loc_long)
        data["dist"] = "{0:.2f}".format(dist)
        
        if 0<dist<=2:
            self.dist1.insert_node(data)
        elif 2<dist<=4:
            self.dist2.insert_node(data)
        elif 4<dist:
            self.dist3.insert_node(data)
    
    def queryDist(self, query):
        dist_level = query[0]
        if dist_level==0:
            return self.dist1.queryPrice(query)
        elif dist_level==1:
            return self.dist2.queryPrice(query)
        else:
            return self.dist3.queryPrice(query)
    
    def printTree(self):
        print("Root")
        print("  - Dist: 0 to 2km")
        self.dist1.printTree()
        print("  - Dist: 2 to 4km")
        self.dist2.printTree()
        print("  - Dist: More than 4km")
        self.dist3.printTree()
        
class Dist:
    """Distance class
    """
    def __init__(self, dist):
        """Creates three price range children each denoting one of the price 
        buckets. The buckets are as follows - 
            * $: Price1
            * $$: Price2
            * $$$: Price3
        """
        self.cap = dist
        self.price_range1 = Rating(dist, "Price1")
        self.price_range2 = Rating(dist, "Price2")
        self.price_range3 = Rating(dist, "Proce3")

    def insert_node(self, data):
        try:
            data["price_level"]
        except:
            data["price_level"] = 2
        if data["price_level"] == 1:
            self.price_range1.insert_node(data)
        elif data["price_level"] == 2:
            self.price_range2.insert_node(data)
        else:
            self.price_range3.insert_node(data)
            
    def queryPrice(self, query):
        price_level = query[1]
        if price_level==0:
            return self.price_range1.queryRating(query)
        elif price_level==1:
            return self.price_range2.queryRating(query)
        else:
            return self.price_range3.queryRating(query)

    
    def printTree(self):
        print("    - Price level : $")
        self.price_range1.printTree()
        print("    - Price level : $$")
        self.price_range2.printTree()
        print("    - Price level : $$$")
        self.price_range3.printTree()
        
class Rating:
    def __init__(self, dist, price_level):
        """Creates three distance children each denoting one of the rating 
        buckets. The buckets are as follows - 
            * 0 to 3: Rating1
            * 3 to 4: Rating2
            * 4 to 5: Rating3
        """
        self.dist = dist
        self.price_level = price_level
        self.ratings1 = Listings(dist, price_level, "rating1")
        self.ratings2 = Listings(dist, price_level, "rating2")
        self.ratings3 = Listings(dist, price_level, "rating3")
        
    def insert_node(self, data):
        try:
            data["rating"]
        except:
            data["rating"] = 3.5
        rating = data["rating"]
        if 0<rating<=3:
            self.ratings1.insert_node(data)
        if 3<rating<=4:
            self.ratings2.insert_node(data)
        else:
            self.ratings3.insert_node(data)


    def queryRating(self, query):
        rating_level = query[2]
        if rating_level==0:
            return self.ratings1.queryListings()
        elif rating_level==1:
            return self.ratings2.queryListings()
        else:
            return self.ratings3.queryListings()
                
    def printTree(self):
        print("      - Rating1: 1 to 3")
        self.ratings1.printTree()
        print("      - Rating2: 3 to 4")
        self.ratings2.printTree()
        print("      - Rating3: 4 and above")
        self.ratings3.printTree()


class Listings:
    """Node class
    """
    
    def __init__(self, dist, price_level, rating):
        self.dist = dist
        self.price_level = price_level
        self.rating = rating
        self.listings = []

    def insert_node(self, data):
        self.listings.append(data)
        #self.printNode(data)

    def printTree(self):
        for listing in self.listings:
            print("        - ",listing["name"])
            #print(f"             - {listing}")

    def queryListings(self):
        return self.listings
                     
    def printNode(self, data):
        print("Name: {},\n Dist: {},\n Rating: {},\n Price Level: {}".format(data["name"],self.dist,self.price_level,self.rating))
        
        
if __name__ == "__main__":
    """Loads small sample json, creates tree with dummy location and prints tree
    """
    import json
    with open('sample_data_for_tree.json', 'r') as f:
        cache_data = json.load(f)
    
    user_loc = (42.269025700396604, -83.72926195271462)
    tree = root(user_loc)   
    
    for listing in cache_data:
        tree.insertlisting(listing)
        
    tree.printTree()