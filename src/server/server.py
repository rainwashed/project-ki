from server.vars import sio
from aiohttp import web
from audio.audio_recog import test_audio_recog, audio_recog
from audio.audio_gen import test_audio_gen, audio_gen
from audio.record import start_recording

@sio.on("connect")
def connect(sid, environ, auth):
    print(f"New server connection from {sid}.")

@sio.on("disconnect")
def disconnect(sid):
    print(f"Lost server connection from {sid}.")

@sio.on("audio_record")
async def audio_record(*args):
    try:
        duration = int(args[1])
    except ValueError:
        duration = 3

    start_recording(duration)

    return True

@sio.on("audio_recog")
async def audio_recog(*args):
    try:
        s = await audio_recog()

        return s
    except Exception as e:
        return str(e)
    
@sio.on("audio_gen")
async def audio_genS(*args):
    try:
        print("calling audio gen")
        print(args)
        await audio_gen(args[1])

        with open("src/cache/model_gen.wav", "rb") as f:
            return f.read()
        
    except Exception as e:
        return str(e)

# Model Tests
@sio.on("model_test-audiorecog")
async def model_test(sid, data):
    print(sid, data)

    (status, time) = await test_audio_recog()

    return status

@sio.on("model_test-audiogen")
async def model_test(sid, data):
    print(sid, data)

    status = await test_audio_gen()

    return status

@sio.on("model_test-llm")
async def model_test(sid, data):
    pass

@sio.on("ping")
async def ping(*args):
    return "pong"

@sio.on("log")
async def log(*args):
    print(args)

    await sio.emit("log_message", args[1])

app = web.Application()

sio.attach(app)

def run():
    web.run_app(app, port=4000)

if __name__ == "__main__":
    run()