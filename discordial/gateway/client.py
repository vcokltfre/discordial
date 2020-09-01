"""
The MIT License (MIT)
Copyright (c) 2020 vcokltfre
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import asyncio
from asyncio.coroutines import coroutine
import websockets
import json
import time

from .intents import Intents
from .resolver import resolve_gateway
from .static import OPCODES
from .dispatcher import Dispatcher


class GatewayClient:
    """ A class to connect to and receive events from the Discord gateway """

    def __init__(self, token: str, intents: Intents = Intents([]), dispatch_all_events: bool = False):
        self.token = token                      # The bot's token to connect to the gateway and API
        self.intents = intents.intents          # The gateway intents the bot should have when connecting to the gateway
        self.gateway = resolve_gateway(token)   # The WSS URI of the gateway

        self.heartbeats = None                  # The amount of heartbeats sent
        self.heartbeat_interval = None          # The interval in miliseconds between client heartbeats
        self.last_heartbeat = None              # The time when the last heartbeat was sent

        self.sequence_id = 0                    # The 'seq' field of the latest event
        self.session_id = None                  # The current session ID
        self.reconnect = False                  # Whether or not the bot shold reconnect or just connect

        self.ws = None                          # The client's websocket connection to the gateway
        self.dispatcher = Dispatcher(dispatch_all_events)   # The client's event dispatcher
        self.loop = asyncio.get_event_loop()    # The asyncio event loop

    def set_callback(self, event_name: str, callback: coroutine):
        """An alias for GatewayClient.dispatcher.set_callback()

        Args:
            callback_name (str): The dispatcher event name
            callback (coroutine): The dispatcher callback coroutine
        """

        self.dispatcher.set_callback(event_name, callback)

    async def create_connection(self):
        """ Connect to the gateway using the retrieved URI """

        self.ws = await websockets.connect(self.gateway['url'])

    async def send(self, op: int, data: object):
        """Send a gateway command to the gateway

        Args:
            op (int): The gateway command opcode
            data (object): The command payload
        """

        data = json.dumps({
            "op": op,
            "d": data
        })

        await self.ws.send(data)

    async def receive(self):
        """ An async loop to receive gateway events """

        await self.create_connection()

        while True:
            data = json.loads(await self.ws.recv())
            #print(data)

            self.sequence_id = data['s'] # Set the sequence id to the one sent by the gateway in case a reconnect is needed

            if data['op'] != 0:
                await self.handle_op(data['op'], data)

            await self.dispatcher.dispatch(data)

    async def handle_op(self, op: int, data: object):
        """Handle a non 0 opecode gateway event, such as HELLO or RECONNECT

        Args:
            op (int): The gateway event opecode
            data (object): The gateway event payload
        """

        if op == OPCODES.HELLO: # Handle a gateway hello
            await self.handle_hello(data)

        elif op == OPCODES.RECONNECT:
            self.ws.close()
            await self.create_connection()

    async def handle_hello(self, data: object):
        """ Handle a gateway hello event

        Args:
            data (object): The hello event payload
        """

        if self.reconnect: # If reconnect has been set to true we need to send the session ID and sequence number too
            payload = {
                "token": self.token,
                "session_id": self.session_id,
                "seq": self.sequence_id
            }

        else:
            payload = {
                "token": self.token,
                "properties": {
                    "$os": "linux",
                    "$broswer": "discordial",
                    "$device": "discordial"
                },
                "intents": self.intents
            }

        opcode = 6 if self.reconnect else 2
        await self.send(opcode, payload)

        self.heartbeat_interval = data['d']['heartbeat_interval']
        self.loop.create_task(self.heartbeat())

    async def heartbeat(self):
        """ Start a heartbeat loop to send heartbeats to the gateway at the interval chosen by the gateway """

        while True:
            await asyncio.sleep(self.heartbeat_interval / 1000) # Sleep for the duration of the heartbeat interval

            await self.send(1, self.heartbeats) # Send the heartbeat with the number of heartbeats sent
            self.last_heartbeat = time.time()

            if self.heartbeats:                                 # Set the number of heartbeats to 1 after the first
                self.heartbeats += 1                            # heartbeat because the gateway requires the first
            else:                                               # payload to be a null value
                self.heartbeats = 1

    def start(self):
        self.loop.run_until_complete(self.receive())