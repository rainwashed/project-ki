import asyncio
from socketio import Client
from time import sleep
from audio.record import open_record_loop
import playsound

sio = Client()

@sio.on("connect")
async def onconnect():
    print("[*] - Client established connection to the backend server")

@sio.on("disconnect")
async def disconnect():
    print("[!] - Client disconnected from the backend server")

sio.connect("http://0.0.0.0:4000")
sio.emit("llm-check_status") # ping to warmup the connection
sio.emit("llm-new_chat") # create a new chat

def start():
    def audio_recog_callback(script: str):
        print("[*] - Finished audio recog; entered callback")
        print(script)
        
        def llm_message_callback(response: str):
            print("[*] - Received response from the conversation bot.")
            print("[!] - {}".format(response))

            def audio_gen_callback():
                print("[*] - Generated voice response. Will play it now.")
                playsound.playsound("src/cache/model_gen.wav", True)

            print("[*] - Generating voice of response.")
            sio.emit("audio_gen", response, callback=audio_gen_callback)
        
        print("[*] - Sending message to the conversation bot")
        sio.emit("llm-send_message", script, callback=llm_message_callback)


    print("[*] - Start audio recog.")
    sio.emit("audio_recog", callback=audio_recog_callback)

def callback():
    print("called back from record")
    start()

iteration = 0
def loop():
    global iteration
    if iteration == 0:
        print("[!] - Hello, my name is Robert. I am an artificial chatbot used for the International Baccalaureate personal project. I am not alive, therefore I cannot provide you with present knowledge. However, I will try to have a conversation with you. It is nice to meet you.")
        playsound.playsound("src/cache/startup.wav")
    print("[?] - Hold [_____SPACE____] when you are ready to speak. Release [______________] when you are finished.")
    open_record_loop(callback=callback)
    ## TODO: Cause loop to occur AFTER whole process is finished and fix adding to iteration
    loop()
    iteration += 1

loop()