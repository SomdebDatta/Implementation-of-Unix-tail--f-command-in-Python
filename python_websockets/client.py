import asyncio
import websockets

async def hello():
    uri = 'ws://localhost:8765'
    async with websockets.connect(uri) as websocket:
        name = input('Whats your name? ')

        await websocket.send(name)
        print(f'Client sent: {name}')

        greeting = await websocket.recv()
        print(f'Client received: {greeting}')

async def counter():
    uri = 'ws://localhost:8765'
    async with websockets.connect(uri) as websocket:
        print('Client connected. Listening for updates...')
        while True:
            ct = await websocket.recv()
            print(f'Client recieved counter value - {ct}')


if __name__ == '__main__':
    # asyncio.run(hello())
    asyncio.run(counter())