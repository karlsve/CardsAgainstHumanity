import asyncio
import json

import websockets as ws


async def test():
    async with ws.connect("ws://localhost:8765/matches") as s:
        await s.send(json.dumps({"method": "create", "matchConfig": {"name": "TestMatch"}}))
        resp = await s.recv()
        tid = json.loads(resp)["id"]
        print(resp)
        await s.send(json.dumps({"method": "list"}))
        resp = await s.recv()
        print(resp)
        async with ws.connect("ws://localhost:8765/match") as gs:
            await gs.send(json.dumps({"method": "connect", "id": tid, "user": {"name": "karlsve"}}))
            resp = await gs.recv()
            print(resp)
            gs.close()
        await s.send(json.dumps({"method": "list"}))
        resp = await s.recv()
        print(resp)
        s.close()


asyncio.get_event_loop().run_until_complete(test())
