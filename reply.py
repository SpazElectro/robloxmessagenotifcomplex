from main import CURRENT_MESSAGE
from mainrequest import *
from notifications import *
from urlbase import *

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
