from server.vars import sio
from aiohttp import web
from audio.audio_recog import test_audio_recog

@sio.on("connect")
def connect(sid, environ, auth):
    print(f"New server connection from {sid}.")

@sio.on("disconnect")
def disconnect(sid):
    print(f"Lost server connection from {sid}.")

@sio.on("model_test")
def model_test(sid, data):
    print(sid, data)

    (status, time) = test_audio_recog()

    return f"Hello there! Status: {status} within {time}s"

app = web.Application()

sio.attach(app)

def run():
    web.run_app(app, port=4000)

if __name__ == "__main__":
    run()