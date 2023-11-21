from sys import exit
from server.vars import sio
from conversation.support_functions import new_chat as mnew_chat, send_chat as msend_chat, ping
if __name__ == "__main__":
    print("This file should be imported, not ran. Cancelling execution.")
    exit()

print("Server extensions connected")

chatid = ""

@sio.on("extension_test")
async def extension_test():
    return "test";

@sio.on("llm-check_status")
def check_status(*args):
    status = ping()
    return status

@sio.on("llm-new_chat")
def new_chat(*args):
    global chatid
    id = mnew_chat()
    chatid = id

    return id

@sio.on("llm-send_message")
def send_chat(*args):
    global chatid
    msg = str(args[1])

    if (chatid == ""):
        return False

    response = msend_chat(msg, chatid)

    return response

sio.on("llm-get_history")
async def get_history():
    pass