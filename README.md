# vcokltfre/discordial

## A lightweight Discord library written in Python

#### A simple example

```py
from discordial import GatewayClient

async def on_message(data):
    print(data['content'])

client = GatewayClient("discord-token")
client.set_callback("on_message_create", on_message)
client.start()
```