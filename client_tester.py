import asyncio
import json

import websockets as ws


async def test():
    async with ws.connect("ws://localhost:8765/matches") as s:
        await s.send("{\"method\": \"create\", \"MatchConfig\": {\"name\": \"TestMatch\"}}")
        resp = await s.recv()
        id = json.loads(resp)["id"]
        print(resp)
        await s.send("{\"method\": \"list\"}")
        resp = await s.recv()
        print(resp)
        async with ws.connect("ws://localhost:8765/match") as gs:
            await gs.send("{{\"method\": \"connect\", \"id\": {0}}}".format(id))
            resp = await gs.recv()
            print(resp)


asyncio.get_event_loop().run_until_complete(test())
