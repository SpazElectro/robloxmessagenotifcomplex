import time

from win10toast_click import ToastNotifier
from dotenv import load_dotenv
from urlbase import *
from mainrequests import *
from notifications import *

load_dotenv()

CHECK_INTERVAL = 1

CURRENT_MESSAGE = None

rbx_request("POST", authurl)

while True:    
    resp = rbx_request("GET", getmessagesurl)
    data = resp.json()

    messageCount = 0

    for message in data["collection"]:
        if not message["isRead"]:
            messageCount += 1

    if messageCount > 0:
        print("You have {} new message(s)".format(messageCount))
        
        for message in data["collection"]:
            if not message["isRead"]:
                CURRENT_MESSAGE = message

                print("{} from {}".format(message["subject"], message["sender"]["name"]))

                send_notification("New Message", "{} from {}".format(message["subject"], message["sender"]["name"]), 4, on_click)
    else:
        print("You have no new messages")

    time.sleep(CHECK_INTERVAL)

