import webbrowser

from main import CURRENT_MESSAGE
from mainrequest import *
from notifications import *
from urlbase import *

def formatMessage(body):
    newBody = body.replace("<br />", "\n")

    return newBody

def open_last_message():
    webbrowser.open(lastmessageurl)

    print("Opened a new tab to view the message.")

def on_click():
    # mark as read
    markedRead = {"messageIds": []}
    markedRead["messageIds"].append(CURRENT_MESSAGE["id"])

    _x = rbx_request("OPTIONS", markreadurl, data=markedRead)
    x = rbx_request("POST", markreadurl, data=markedRead)

    print(f"\"{CURRENT_MESSAGE['sender']['displayName']}\" (\"{CURRENT_MESSAGE['sender']['name']}\") sent you a message containing: \n")
    print(formatMessage(CURRENT_MESSAGE["body"]))

    send_notification("Content", "{}".format(formatMessage(CURRENT_MESSAGE["body"])), 15, reply)
