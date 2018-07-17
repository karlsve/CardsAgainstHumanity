from datetime import datetime

from wsl import Endpoint
from wsl import WebSocketServer

cah_ws = WebSocketServer("localhost", 8765)
matches = []


@cah_ws.endpoint("/matches")
class Matches(Endpoint):
    @cah_ws.method()
    async def list(self, gm):
        await self.send(matches)

    @cah_ws.method("matchConfig")
    async def create(self, gm):
        mc = gm["matchConfig"]
        mid = len(matches)
        match = {
            "config": mc,
            "player": [],
            "deck": {},
            "id": mid,
            "creation_time": datetime.now().time()
        }
        matches.insert(mid, match)
        await self.send({"type": "match_created", "id": mid})


@cah_ws.endpoint("/match")
class Match(Endpoint):
    @cah_ws.method("id", "user")
    async def connect(self, gm):
        if 0 <= gm["id"] < len(matches):
            match = matches[gm["id"]]
            u = {
                "config": gm["user"],
                "socket": self.socket
            }
            match["player"].append(u)
            await self.send({"type": "connected", "match": match})
        else:
            await self.send({"error": "Match {0} not found.".format(gm["id"])})


@cah_ws.endpoint("/decks")
class Decks(Endpoint):
    async def list(self, gm):
        pass


@cah_ws.endpoint("/deck")
class Deck(Endpoint):
    @cah_ws.method("id")
    async def get(self, gm):
        print(gm["id"])
        pass

    @cah_ws.method("deckConfig")
    async def create(self, gm):
        pass


cah_ws.start()
