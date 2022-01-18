import time
import classes.Controller as cont
import asyncio
from dotenv import load_dotenv

load_dotenv('.env')

async def main():
    controller = cont.Controller()
    await controller.run()

while(True):
    time.sleep(5)
    asyncio.run(main())