import asyncio
import websockets


async def handler(websocket):
    async for message in websocket:
        print(f"Web Socket - Message reçu: {message}")

async def ouvrir_websocket():
    print("lancement serveur web socket")
    async with websockets.serve(handler, "localhost", 8000):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(ouvrir_websocket())