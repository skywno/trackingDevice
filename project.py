import os
import time
import requests
import uuid
from time import sleep
from pymongo import MongoClient
import datetime
from pymongo import ReturnDocument
import pprint

try:
    import sys
    import tty
    import termios

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch    

except ImportError:
    import msvcrt

    def getch():
        return msvcrt.getch()

def main():
    url = "https://elecdesign.org.aalto.fi/tracker/api/" 
    payload = "{\"uuid\": \"" + str(uuid.uuid1()) +  "\", \"c\": \"1\"}"
    headers = {
      'Content-Type': 'application/json'
    }
    polling = True
    testing = False	
    tracking = False
    
    oldTime = time.time()
    count = 0
    
    client = MongoClient('localhost', 27017)
    db = client.project
    #collection = db.tracking
    trackername = "Example Device 1"

    post = {"trackerName": "Example Device 1", "StartDate": datetime.datetime.today(), "endDate" : 'unknown'}
    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    pprint.pprint(posts.find_one())
    
    while True: # this is called the 'main loop' = it keeps repeating until things shut down
        if polling == True:
            if time.time() - oldTime > 1:
                sleep(0.5)
                oldTime = time.time()
                response = requests.request("POST", url, headers=headers, data = payload)
                print(response.text.encode('utf8'))
                print(response)
                dict = response.json()
                print(dict['msg'])
                if dict['msg'] == "setup":
                    continue
                elif dict['msg'] == "test":
                    polling = False
                    testing = True
                    continue
                elif dict['msg'] == "track" or dict['msg'] == "device expected to be in tracking mode - message wrongly formatted":
                    polling = False
                    testing = False
                    tracking = True
                else:
                    continue
                     
        elif testing == True:
            while dict['msg'] == "test":
                payload = "{\"uuid\": \"" + str(uuid.uuid1()) +  "\", \"n\": \"0\"}" 
                char = getch()
                if (char == "p"):
                    print("stop!")
                    exit(0)
                elif (char == "b"):
                    print("button b pressed")
                    time.sleep(0.5)
                    count += 1 
                if time.time() - oldTime > 15:
                    sleep(1) # See above, use with care!
                    oldTime = time.time()
                    response = requests.request("POST", url, headers=headers, data = payload)
                    print(response.text.encode('utf8'))  
                    
            if dict['msg'] == "setup":
                polling = True
                testing = False
                continue
            elif dict['msg'] == "test":
                continue
            elif dict['msg'] == "track":
                polling = False
                testing = False
                tracking = True
        elif tracking == True:       
            while True:
                payload = "{\"uuid\": \"" + str(uuid.uuid1()) +  "\", \"n\": \"0\"}" 
                char = getch()
                if (char == "p"):
                    print("stop!")
                    exit(0)
                elif (char == "b"):
                    print("button b pressed")
                    time.sleep(0.5)
                    count += 1 
                if time.time() - oldTime > 15:
                    sleep(1) # See above, use with care!
                    oldTime = time.time()
                    response = requests.request("POST", url, headers=headers, data = payload)
                    print(response.text.encode('utf8'))                    
                    #find a single document that has the tracker name: 'example device 1' and update its day 1 value.
                    posts.find_one_and_update({"trackerName": "Example Device 1"}, {'$inc': {'day_one': count}}, return_document=ReturnDocument.AFTER)
                    count = 0

                                      
        else:
            continue 
        
if __name__ == "__main__":
    main()
    
