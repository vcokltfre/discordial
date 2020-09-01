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

shifts = {
    "GUILDS": 0,
    "GUILD_MEMBERS": 1,
    "GUILD_BANS": 2,
    "GUILD_EMOJIS": 3,
    "GUILD_INTEGRATIONS": 4,
    "GUILD_WEBHOOKS": 5,
    "GUILD_INVITES": 6,
    "GUILD_VOICE_STATES": 7,
    "GUILD_PRESENCES": 8,
    "GUILD_MESSAGES": 9,
    "GUILD_MESSAGE_REACTIONS": 10,
    "GUILD_MESSAGE_TYPING": 11,
    "DIRECT_MESSAGES": 12,
    "DIRECT_MESSAGE_REACTIONS": 13,
    "DIRECT_MESSAGE_TYPING": 14
}


class Intents:
    """ A class to easily construct intents integers """

    def __init__(self, intents: list):
        self.intents = 0

        if len(intents) == 0 or "ALL" in intents:
            intents = [
                "GUILDS",
                "GUILD_BANS",
                "GUILD_EMOJIS",
                "GUILD_INTEGRATIONS",
                "GUILD_WEBHOOKS",
                "GUILD_INVITES",
                "GUILD_VOICE_STATES",
                "GUILD_MESSAGES",
                "GUILD_MESSAGE_REACTIONS",
                "GUILD_MESSAGE_TYPING",
                "DIRECT_MESSAGES",
                "DIRECT_MESSAGE_REACTIONS",
                "DIRECT_MESSAGE_TYPING"
            ]

        for intent in intents:
            intent = intent.upper()
            if intent in shifts:
                self.intents += 1 << shifts[intent]
            else:
                raise ValueError(f"Invalid Intent: {intent}")