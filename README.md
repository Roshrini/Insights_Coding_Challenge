Insight Data Engineering - Coding Challenge Solution Approach
===============================================================

This solution was implemented in Python 2.7. I used following libraries to implement it
import sys
import json       - Json file parsing
import time       - For converting time to epoch time (Easy for time comparison)
import itertools  - For iterating through directory
from collections import defaultdict - To use directory data structure

You can find code in /src/average_degree.py
It computes average degree of twitter hashtags graph.

Approach taken to solve the problem:
1) Parse the json files. Used Json module for that. Took care of the missing keys in the parsed data.
2) Extracted hashtags and created_by values for each tweet
3) Used set and did sorting in the tuples of hashtags to avoid duplicates
4) To find the edges from nodes, used itertools.combinations. It gives all the possible combinations of edges
   for each tweet.
5) Implemented sliding window by maintaining a start pointer for starting point of 60 seconds window and
   end point is considered as index. As new tweet is processed, time is checked if it is under 60 secs or not.
   If not, new tweet is added to the list and tweet from start pointer
   is removed from list and start pointer is incremented. Start time is also changed accordingly.
6) Implemented graph as a class and used dictionary data structure to keep connected adges
7) Used set and did sorting in the tuples of hashtags to avoid duplicate tuples in dictionary values.
8) Calculated average degree of the graph by iterating through the dictionary. Size of set as value
   corresponding to each key in dictionary gives degree for that particular node. Dividing it by total keys in
   dictionary will give average degree of graph.
9) Writes output the output file.
10) My approach takes care of deletion of old tweets (more than 60 secs old), broken graphs, out of order
 	arrival of tweets

Some important things I took care of are as follows:
1) Boundary conditions. Empty hashtags or created_at values
2) Null value checks to avoid errors
3) Used set and did sorting in the tuples of hashtags to avoid duplicates
5) Tested the code with some sample input. I have included sample in tweet_input/tweets_2.txt
4) Commented the code for better understanding

I have included output I got after processing /data-gen/tweets.txt in /data-gen/tweets_op.txt