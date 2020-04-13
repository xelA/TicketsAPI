import time
import secrets
import enum
import json

from jsonschema import validate


class TicketSource(enum.IntEnum):
    unknown = 0
    valid = 1
    approved = 2


class Ticket:
    def __init__(self, payload=None, db=None, expire: int = 86400):
        self.payload = payload
        self.db = db
        self.expire = expire
        self.re_discord_id = "^[0-9]{14,19}$"

    @property
    def generate_id(self):
        """ Generate random ID with Python.secrets """
        id = secrets.token_urlsafe(10)
        return id

    def fetch_ticket(self, ticket_id: str):
        """ Fetch ticket from SQLite database """
        if not self.db:
            print("This function needs DB variable")

        data = self.db.fetchrow(
            "SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,)
        )

        return data

    def attempt_post(self):
        """ Attempt to post JSON payload to SQLite database """
        if not self.db or not self.payload:
            print("This function needs both payload and DB")

        code, output = self.validation()
        if code != 200:
            return (code, output)

        query = "INSERT INTO tickets " \
                "(ticket_id, guild_id, author_id, context, submitted_by, created_at, logs, expire, confirmed_by) " \
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

        right_now = int(time.time())
        ticket_id = self.generate_id

        try:
            self.db.execute(
                query, (ticket_id, int(output["guild_id"]), int(output["author_id"]), output["context"],
                int(output["submitted_by"]), int(output["created_at"]), json.dumps(output), right_now + self.expire, int(output["confirmed_by"]))
            )
        except Exception as e:
            print(e)
            return (500, "Internal server error... contact site owner.")

        return (code, ticket_id)

    def validation(self):
        """ Validate the payload sent to POST """
        if not self.payload:
            print("This function needs payload")

        json_validation = {
            "definitions": {
                "content_entry": {
                    "type": "object",
                    "properties": {
                        "msg": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                        "edited": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                        "deleted": {"type": "boolean"},
                        "content": {"type": "string"}
                    },
                    "required": ["msg"]
                },

                "users_entry": {
                    "type": "object",
                    "propertyNames": {"pattern": self.re_discord_id},
                    "patternProperties": {
                        f"{self.re_discord_id}": {
                            "type": "object",
                            "properties": {
                                "username": {"type": "string"},
                                "avatar": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                                "badge": {"anyOf": [{"type": "string"}, {"type": "null"}]}
                            },
                            "required": ["username", "avatar", "badge"]
                        }
                    }
                },

                "messages": {
                    "type": "object",
                    "properties": {
                        "author": {"type": "string"},
                        "timestamp": {
                            "type": "number",
                            "minimum": 0
                        },
                        "content": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/content_entry"}
                        }
                    },
                    "required": ["author", "timestamp", "content"]
                }
            },

            "type": "object",
            "properties": {
                "context": {"type": "string"},
                "channel_name": {"type": "string"},
                "created_at": {"type": "number", "minimum": 0},
                "submitted_by": {"type": "string", "pattern": self.re_discord_id},
                "confirmed_by": {"type": "string", "pattern": self.re_discord_id},
                "author_id": {"type": "string", "pattern": self.re_discord_id},
                "guild_id": {"type": "string", "pattern": self.re_discord_id},
                "users": {"$ref": "#/definitions/users_entry"},
                "messages": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/messages"}
                }
            },
            "required": ["channel_name", "guild_id", "created_at", "author_id", "users", "messages", "submitted_by", "context", "confirmed_by"]
        }

        try:
            validate(self.payload, schema=json_validation)
        except Exception as e:
            return (400, e)

        return (200, self.payload)
