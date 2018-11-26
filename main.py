import asyncio

from gpustat import new_query

import config
import socketio
from sanic import Sanic, response

app = Sanic()
sio = socketio.AsyncServer(async_mode='sanic')
sio.attach(app)


@app.route('/')
async def index(request):
    return await response.file('index.html')


async def update_gpu_stats():
    while True:
        await asyncio.sleep(1)
        # print(len(sio.manager.rooms))
        if len(sio.manager.rooms) > 0:
            gpu_stats = new_query()
            # print(gpu_stats.jsonify())
            await sio.emit('gpustat', gpu_stats.jsonify())
        # print(len(app.sio.rooms))


if __name__ == "__main__":
    app.add_task(update_gpu_stats())
    app.run(host="0.0.0.0", port=8000)
