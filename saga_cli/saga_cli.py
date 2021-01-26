import requests
import json
import webbrowser
import sys
import argparse

PROTOCOL = 'http'
PORT = '8090'

#URL = 'saga-ra2-api.jz.demilitarised.zone'
URL = 'localhost'

def print_section_break():
    print("===========================")

def get_choice():
    topics = []

    API_PATH = '/api/recommend'

    res = requests.get(PROTOCOL+'://'+URL+':'+PORT+API_PATH)
    topics = json.loads(res.content)

    print("Select a topic out of: ")
    for topic in range(0, len(topics)):
        print("["+str(topic)+"]: "+topics[topic]['topic'])
    selection = input()

    return topics[int(selection)]['topic']

def get_free_time():
    print("How much free time: ")
    selection = input()
    return selection

def query_db(topic_choice, free_time):
    API_PATH = '/api/recommend'+'?topic='+topic_choice+'&minutes_reading='+free_time
    res = requests.get(PROTOCOL+'://'+URL+':'+PORT+API_PATH)
    url = json.loads(res.content)
    return url['url']

def recommend(topic_choice, free_time):

    url = query_db(topic_choice, free_time)

    print("Would you like to read")
    print(url)
    print("(Y/N):")
    selection = input()
    
    #Maybe do Y, N or other here
    
    if selection.upper() == "Y":
        webbrowser.open(url,new=2)
    else:
        print_section_break()
        recommend(topic_choice)

def main():
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("next", help="Number of links to process per run")
    parser.add_argument("--free-time", help="Amount of free time")
    parser.add_argument("--topic", help="Topic to read")
    args = parser.parse_args()

    topic_choice = ''
    free_time = ''

    if args.next:
        if not args.topic:
            topic_choice = get_choice()
        else:
            topic_choice = args.topic
        if not args.free_time:
            free_time = get_free_time()
        else:
            free_time = args.free_time

        #Validate free time int here
        
        print_section_break()
        recommend(topic_choice, free_time)
        print_section_break()
    
    exit(0)

main()