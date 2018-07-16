# CardsAgainstHumanity.py
A simple CardsAgainstHumanity implementation in python to act as a websocket server for a corresponding AngularJS App.

## wgl.py
This is the websocket and database handling implementation.

Example usage

```python
import asyncio
from wgl import GameServer
from wgl import Endpoint
someApp = GameServer("cah", "localhost", 8765) 
# GameServer(dbname, ip/hostname, port)
@someApp.endpoint("/somepath")
class SomeEndpoint(Endpoint):
    def init(self):
        pass # Some init function
        
    @someApp.method("requiredParameter")
    async def someMethod(self, gm):
        pass # do something
```
