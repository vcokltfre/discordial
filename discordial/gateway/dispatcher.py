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

from asyncio.coroutines import coroutine
from logging import log


class Dispatcher:
    """ A class to dispatch websocket events """

    def __init__(self, all_events=False):
        self.all_events = all_events
        self.events = {
            "on_channel_create": self.null_dispatch,
            "on_channel_update": self.null_dispatch,
            "on_channel_delete": self.null_dispatch,
            "on_channel_pins_update": self.null_dispatch,
            "on_guild_create": self.null_dispatch,
            "on_guild_update": self.null_dispatch,
            "on_guild_delete": self.null_dispatch,
            "on_guild_ban_add": self.null_dispatch,
            "on_guild_ban_remove": self.null_dispatch,
            "on_guild_emojis_update": self.null_dispatch,
            "on_guild_integrations_update": self.null_dispatch,
            "on_guild_member_add": self.null_dispatch,
            "on_guild_member_remove": self.null_dispatch,
            "on_guild_member_update": self.null_dispatch,
            "on_guild_members_chunk": self.null_dispatch,
            "on_guild_role_create": self.null_dispatch,
            "on_guild_role_update": self.null_dispatch,
            "on_guild_role_delete": self.null_dispatch,
            "on_invite_create": self.null_dispatch,
            "on_invite_delete": self.null_dispatch,
            "on_message_create": self.null_dispatch,
            "on_message_update": self.null_dispatch,
            "on_message_delete": self.null_dispatch,
            "on_message_delete_bulk": self.null_dispatch,
            "on_message_reaction_add": self.null_dispatch,
            "on_message_reaction_remove": self.null_dispatch,
            "on_message_reaction_remove": self.null_dispatch,
            "on_message_reaction_remove_emoji": self.null_dispatch,
            "on_presence_update": self.null_dispatch,
            "on_typing_start": self.null_dispatch,
            "on_user_update": self.null_dispatch,
            "on_voice_state_update": self.null_dispatch,
            "on_voice_server_update": self.null_dispatch,
            "on_webhooks_update": self.null_dispatch,
            "on_ready": self.null_dispatch,
            "on_raw_socket_receive": self.null_dispatch
        }

    async def null_dispatch(self, data: object):
        """A non-functional dispatch handler to void unhandled events

        Args:
            data (object): Dispatcher payload
        """

    async def dispatch(self, data: object):
        """A dispatcher for async events coming from the gateway

        Args:
            data (object): Gateway event payload
        """

        try:
            if self.all_events:
                await self.events["on_raw_socket_receive"](data)

            if data['t']: # Only dispatch discord events, rather than all events including gateway
                event_name = data['t'].lower().replace(' ', '_')
                event_name = f"on_{event_name}"

                await self.events[event_name](data['d'])

        except Exception as e:
            log(30, str(e), exc_info=True)

    def set_callback(self, event_name: str, callback: coroutine):
        """Set a dispatcher callback for a certain event to a given coroutune

        Args:
            event_name (str): The dispatcher event name
            callback (coroutine): The callback coroutine
        """

        if event_name in self.events:
            self.events[event_name] = callback
        else:
            raise ValueError(f"Invalid dispatcher event name: {event_name}")