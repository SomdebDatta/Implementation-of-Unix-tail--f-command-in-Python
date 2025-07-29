import asyncio
import websockets
from tail_string import Tail

async def counter(websocket):
    ct = 0
    while True:
        resp = f'Counter is at {ct}'
        print(resp)
        await websocket.send(resp)
        ct += 1
        await asyncio.sleep(3)

async def fetch_lines(websocket):
    t = Tail('app2.log', n=5)
    while True:
        if t.check_file_modified():
            for lines in t.yield_last_n_lines():
                print(f'Websocket is sending lines - {lines}')
                await websocket.send(lines)
        await asyncio.sleep(t.secs)


async def main():
    async with websockets.serve(fetch_lines, 'localhost', 8765):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())