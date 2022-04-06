import time
import requests
import os
import webbrowser

from win10toast_click import ToastNotifier
from dotenv import load_dotenv

load_dotenv()

session = requests.session()

CHECK_INTERVAL = 1

ROBLOSECURITY = os.getenv("ROBLOSECURITY")

CURRENT_MESSAGE = None

authurl = "https://auth.roblox.com/v2/logout"
markreadurl = "https://privatemessages.roblox.com/v1/messages/mark-read"
getmessagesurl = "https://privatemessages.roblox.com/v1/messages?pageNumber=1&pageSize=5&messageTab=Inbox"
sendmessageurl = "https://privatemessages.roblox.com/v1/messages/send"

lastmessageurl = "https://www.roblox.com/my/messages/#!/sent?messageIdx=0"

session.cookies[".ROBLOSECURITY"] = ROBLOSECURITY

def rbx_request(method, url, **kwargs):
    request = session.request(method, url, **kwargs)
    method = method.lower()
    if (method == "post") or (method == "put") or (method == "patch") or (method == "delete"):
        if "X-CSRF-TOKEN" in request.headers:
            session.headers["X-CSRF-TOKEN"] = request.headers["X-CSRF-TOKEN"]
            if request.status_code == 403:  # Request failed, send it again
                request = session.request(method, url, **kwargs)
    return request

def formatMessage(body):
    newBody = body.replace("<br />", "\n")

    return newBody

def send_notification(title, message, duration, callback):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=duration, callback_on_click=callback, threaded=False)

def open_last_message():
    webbrowser.open(lastmessageurl)

    print("Opened a new tab to view the message.")

def reply():
    sending = input("What do you want to reply with? ")

    body = {
        "userId": 0, # useless
        "subject": "", # useless
        "body": sending,
        "recipientId": CURRENT_MESSAGE["sender"]["id"],
        "replyMessageId": CURRENT_MESSAGE["id"],
        "includePreviousMessage": False
    }

    print(f"Replying with {sending}...")

    sendMessageRequest = rbx_request("POST", sendmessageurl, data=body)
    
    print(f"{sendMessageRequest.json()['shortMessage']}: {sendMessageRequest.json()['message']}")

    send_notification(sendMessageRequest.json()["shortMessage"], sendMessageRequest.json()["message"], 3, open_last_message)

def on_click():
    # mark as read
    markedRead = {"messageIds": []}
    markedRead["messageIds"].append(CURRENT_MESSAGE["id"])

    _x = rbx_request("OPTIONS", markreadurl, data=markedRead)
    x = rbx_request("POST", markreadurl, data=markedRead)

    print(f"\"{CURRENT_MESSAGE['sender']['displayName']}\" (\"{CURRENT_MESSAGE['sender']['name']}\") sent you a message containing: \n")
    print(formatMessage(CURRENT_MESSAGE["body"]))

    send_notification("Content", "{}".format(formatMessage(CURRENT_MESSAGE["body"])), 15, reply)


rbx_request("POST", "https://auth.roblox.com/")

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

