from conversation.config import cai, caiCharCode
from json import dumps, loads

# call a ping to warm up the server

tgt = cai.chat.get_chat(caiCharCode)["participants"][0]["user"]["username"] if not cai.chat.get_chat(caiCharCode)[
    "participants"][0]["is_human"] else cai.chat.get_chat(caiCharCode)["participants"][1]["user"]["username"]


def ping() -> bool:
    o = cai.ping()

    return o["status"] == "pong"

def new_chat() -> str:
    r = cai.chat.new_chat(char=caiCharCode)
    x = dumps(r)
    y = loads(x)

    return y["external_id"]


def send_chat(msg: str, history_id: str) -> str:
    msg = cai.chat.send_message(history_id=history_id, text=msg,
                                tgt=tgt)

    x=dumps(msg)
    y=loads(x)

    return y["replies"][0]["text"]
