import asyncio
import uvicorn
import websockets

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

latest_value = 'Waiting for counter...'


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/get_counter", response_class=PlainTextResponse)
async def get_counter():
    return latest_value


async def counter_client():
    global latest_value
    uri = 'ws://localhost:8765'
    try:
        async with websockets.connect(uri) as websocket:
            print('Client connected. Listening for updates...')
            while True:
                ct = await websocket.recv()
                print(f'Client received counter value - {ct}')
                latest_value = ct
    except Exception as e:
        print(f'Websocket connection failed: {e}')


async def main():
    config = uvicorn.Config('fastapi_client:app', host='127.0.0.1', port=5000, log_level='info')
    server = uvicorn.Server(config)

    await asyncio.gather(
        counter_client(),
        server.serve()
    )

if __name__ == '__main__':
    asyncio.run(main())