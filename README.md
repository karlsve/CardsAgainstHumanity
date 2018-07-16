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

    @someApp.method()
    async def someMethod(self, gm):
        pass # Method without required parameters
        
    @someApp.method("requiredParameter")
    async def someOtherMethod(self, gm):
        await self.send({"sent":gm["requiredParameter"]})
```

The client can then connect to the endpoint `ws://localhost:8765/somepath`.
The methods are called by sending a JSON object with the appropriate method name e.g.
```json
{
    "method": "someMethod"
}
{
    "method": "someOtherMethod",
    "requiredParameter": true
}
```