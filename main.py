from sanic import Sanic, response
import socketio
import asyncio

app = Sanic()
sio = socketio.AsyncServer(async_mode='sanic')
sio.attach(app)


@app.route('/')
async def index(request):
    return await response.file('index.html')


async def nvidia_smi():
    while True:
        await asyncio.sleep(1)
        print(len(sio.manager.rooms))
        if len(sio.manager.rooms) > 0:
            await sio.emit('nvidia-smi', [])
        # print(len(app.sio.rooms))


if __name__ == "__main__":
    app.add_task(nvidia_smi())
    app.run(host="127.0.0.1", port=8000)
