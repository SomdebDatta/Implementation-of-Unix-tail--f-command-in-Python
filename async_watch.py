import asyncio
from watchgod import awatch, Change


async def main():
    async for changes in awatch('hello.txt'):
        for change_type, file_path in changes:
            if change_type == Change.modified:
                print(f'{file_path} was modified!')


if __name__ == '__main__':
    asyncio.run(main())