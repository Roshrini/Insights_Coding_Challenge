# example of program that calculates the average degree of hashtags
import sys
import json
import time
import itertools
from collections import defaultdict

class Graph(object):
    def __init__(self,tweet_data):
        # using defaultdict to save graph structure and set is used as a value as it removes duplicates
        self._graph = defaultdict(set)
        self.add_edges_graph(tweet_data)

    def add_edges_graph(self,tweet_list):
        # Adding edges to the graph from tweets both ways as it will make calculation of average degree easy
        for edges_list in tweet_list:
            if edges_list is not None:
                for edge in edges_list:
                    node1 = edge[0]
                    node2 = edge[1]
                    self._graph[node1].add(node2)
                    self._graph[node2].add(node1)

#convert timestamp of tweet to epoch time
def get_timestamp(parsed_json):
    if 'created_at' in parsed_json:
        created_at = parsed_json['created_at']
        return int(time.mktime(time.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")))

def get_hashtags(parsed_json):
    hashtags=[]
    # Null check done
    if 'entities' in parsed_json:
        if 'hashtags' in parsed_json['entities']:
            for entry in parsed_json['entities']['hashtags']:
                hashtags.append(entry['text'])
            # This gives combinations of elements in the list. base is 2
            hashtags = list(itertools.combinations(hashtags,2))
    return hashtags

def sorting(hashtags_list):
    sorted_tuple=[]
    # sorting tuples. It will also avoid duplicates
    if hashtags_list is not None:
        for key in hashtags_list:
            sorted_tuple.append((sorted(key)[0],sorted(key)[1]))
    return sorted_tuple

def parseFile(tweet_input_file):
    data = []
    with open(tweet_input_file) as tweet_input:
        for line in tweet_input:
            # using json parser to get key and values
            parsed_json = json.loads(line)
            # get hashtags from parsed data
            hashtags_list = get_hashtags(parsed_json)
            # sorting nodes inside a tuple
            sorting(hashtags_list)
            # Getting parsed data in form of list of tuples of timestamp and list of edges
            data.append((get_timestamp(parsed_json),sorting(hashtags_list)))
    return data

def average_degree(graph):
    graph_dict = graph._graph
    total =0
    cnt = 0
    # Iterate through the dictionary to calculate average degree. Size of set as value corresponding to
    # each key in dictionary gives degree for that particular node
    for key,value in graph_dict.iteritems():
        total = total + len(value)
        cnt=cnt+1
    # DivideByZero exception checked
    if cnt!=0:
        avg_degree = "{0:.2f}".format(float(total)/cnt)
    else:
        avg_degree = "{0:.2f}".format(0)
    return avg_degree

def output_file_writer(avg_degree,tweet_output_file):
    # Write and append output to the output file
    f = open(tweet_output_file,'a')
    f.write(str(avg_degree)+ "\n")
    f.close()

def slidingWindow(tweet_data, tweet_output_file):
    current_tweets = []
    # Maintaining a start pointer for starting point of 60 seconds window and end point is considered as index
    # As new tweet is processed, time is checked if it is under 60 secs or not. If not, new tweet is added to
    # the list, tweet from start pointer
    # is removed from list and start pointer is incremented. Start time is also changed accordingly

    # Processing first tweet from file
    if tweet_data is not None:
        start_time = tweet_data[0][0]
        start_ptr = 0
        current_tweets.append(tweet_data[0][1])
        g = Graph(current_tweets)
        avg_degree = average_degree(g)
        output_file_writer(avg_degree,tweet_output_file)

    # Processing rest of the tweets from file
    for index in range(1,len(tweet_data)):
        end_time = tweet_data[index][0]
        # If time is None check
        if end_time is not None:
            if(end_time-60<=start_time):
                current_tweets.append(tweet_data[index][1])
            else:
                # Deletion of old tweets is taken care of in this block
                current_tweets.append(tweet_data[index][1])
                current_tweets.remove(tweet_data[start_ptr][1])
                start_ptr = start_ptr+1
                start_time = tweet_data[start_ptr][0]

        # For the new fresh tweets graph is build and modified
        g = Graph(current_tweets)
        # Calculates average degree
        avg_degree = average_degree(g)
        # Write output to the file
        output_file_writer(avg_degree,tweet_output_file)

def main():
    tweet_input_file = sys.argv[1]
    tweet_output_file = sys.argv[2]
   #  tweet_input_file = "/Users/roshaninagmote/PycharmProjects/coding-challenge/data-gen/tweets.txt"
   #  tweet_output_file = "/Users/roshaninagmote/PycharmProjects/coding-challenge/data-gen/tweets_op.txt"

    # tweet_input_file = "/Users/roshaninagmote/PycharmProjects/coding-challenge/insight_testsuite/tests/test-2-tweets-all-distinct/tweet_input/tweets.txt"
    # tweet_output_file = "/Users/roshaninagmote/PycharmProjects/coding-challenge/insight_testsuite/tests/test-2-tweets-all-distinct/tweet_output/output.txt"

   # tweet_input_file = "/Users/roshaninagmote/PycharmProjects/coding-challenge/insight_testsuite/tests/test-2-tweets-all-distinct/tweet_input/tweets_2.txt"
    #tweet_output_file = "/Users/roshaninagmote/PycharmProjects/coding-challenge/insight_testsuite/tests/test-2-tweets-all-distinct/tweet_output/output_2.txt"
    # Parse json file
    tweet_data = parseFile(tweet_input_file)
   # Sliding window is taken care of here
    slidingWindow(tweet_data,tweet_output_file)

if __name__ == "__main__":
    main()