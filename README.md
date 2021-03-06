# CardsAgainstHumanity.py
A simple CardsAgainstHumanity implementation in python to act as a websocket server for a corresponding AngularJS App.

## wsl.py
This is the websocket implementation.

Sample usage
```python
import asyncio
from wsl import WSServer
from wsl import Endpoint

someApp = WSServer("localhost", 8765)
# WSServer(ip/hostname, port)

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
The methods are called by sending a JSON object with the appropriate method name e.g.:
```json
{
    "method": "someMethod"
}
{
    "method": "someOtherMethod",
    "requiredParameter": true
}
```
