# -*- coding: utf-8 -*-
"""follower_network_collector.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1T0ED71rbhiNF8HG-769aBqA0zZAJodcd
"""

#This notebook builds a follower network for a set of users
#first import the helper functions 
from helper_follower_network_crawler import *
import sqlite3
import pandas as pd
import random

#COLLECT FOLLOWING NETWORK
#Get the following for a set of screen names
#Filename where we will store the list of following (ends with .csv)
max_following = 2000  #maximum number of following to get per user(10 minutes for 1000 users)
max_users = int(1e4)  #maximum number of users you will build the following network for
FilenameTweetDatabase = "ReopenAmerica.db" 
FilenameFollowingNetwork = "followingnetwork_ReopenAmerica.csv"



print("Tweets will be loaded from database file %s"%FilenameTweetDatabase)
print("Follower network saved to file %s"%FilenameFollowingNetwork)

FilenameFollowingNetworkGpickle = FilenameFollowingNetwork.replace(".csv",".gpickle")
print("Follower network graph object saved to file %s"%FilenameFollowingNetworkGpickle)

print("We will collect maximum %s users, maximum %s following per user"%(max_users,max_following))
#ScreenNames is a list of the screen names you want to build the network of
#Define ScreenNames this way if you want to write the names by hand
#ScreenNames = ["zlisto"]

#get the list of screen_names
conn = sqlite3.connect("%s"%FilenameTweetDatabase)
df_screen_name = pd.read_sql_query("SELECT screen_name FROM tweet", conn)
ScreenNamesAll = list(set([row[0] for row in df_screen_name.values.tolist()]))  #remove duplicate users
nusers =  len(set(ScreenNamesAll))  #total number of unique users in tweet database


#only keep max_users
if max_users<nusers:
    #ScreenNames = ScreenNamesAll[0:max_users]  #take first max_users from list
    ScreenNames = random.sample(ScreenNames,max_users)  #take random sample from list

else:
    ScreenNames = ScreenNamesAll

print("%s users in entire tweet database\nWe will build the following network for %s of them"%(nusers,len(ScreenNames)))
print("\nHere are some of your screen names:%s"%ScreenNames[0:10])

#This function collects the following of each person in ScreenNames 
#and saves it to an Excel file (really a csv file)

#spot in ScreenNames to start your crawler from in case it crashes
#start_index = 0 for a fresh network
start_index = 0 

#temp is the list of names you will collect following for.  
#this list starts at the start_index (we do this in case your code crashes
#you can start up where you left off)
#Collection rate ~ 100 screen names per minute
temp = ScreenNames[start_index:]  
print("starting at %s"%temp[start_index])
get_friends(temp,FilenameFollowingNetwork,max_following)

#This function writes the following network to a networkx object so we can analyze it
G = write_friends_graph_tweets_networkx(ScreenNames,FilenameFollowingNetwork,FilenameFollowingNetworkGpickle)

