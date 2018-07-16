from wgl import Endpoint
from wgl import GameServer

cah = GameServer("cah", "localhost", 8765)
matches = []


@cah.endpoint("/matches")
class Matches(Endpoint):

    @cah.method()
    async def list(self, gm):
        await self.send(matches)

    @cah.method("MatchConfig")
    async def create(self, gm):
        gc = gm["MatchConfig"]
        id = len(matches)
        matches.insert(id, {"config": gc, "id": id})
        await self.send({"type": "match_created", "id": id})


@cah.endpoint("/match")
class Match(Endpoint):
    @cah.method("id")
    async def connect(self, gm):
        if 0 <= gm["id"] < len(matches):
            await self.send(matches[gm["id"]])
        else:
            await self.send({"error": "Match {0} not found.".format(gm["id"])})


@cah.endpoint("/decks")
class Decks(Endpoint):
    async def list(self, gm):
        pass


@cah.endpoint("/deck")
class Deck(Endpoint):
    @cah.method("id")
    async def get(self, gm):
        print(gm["id"])
        pass

    @cah.method("DeckConfig")
    async def create(self, gm):
        pass


cah.start()
