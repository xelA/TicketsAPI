import json
import time
import os

from sanic import response, Sanic
from datetime import datetime, timedelta
from sanic_jinja2 import SanicJinja2
from sanic_scheduler import SanicScheduler, task
from utils import sqlite, tickets

app = Sanic()
app.static('/static', './static')

scheduler = SanicScheduler(app)
jinja = SanicJinja2(app)

db = sqlite.Database()
db.create_tables()  # Attempt to create table(s) if not exists already.

config = json.load(open("config.json", "r"))


@app.route("/")
@jinja.template("index.html")
async def index(request):
    return {"test": "This is a nice test"}


@task(timedelta(seconds=60))
def delete_old_tickets(app):
    """ Delete old ticket entries for privacy reasons """
    db.execute("DELETE FROM tickets WHERE ? > expire", (int(time.time()),))


@app.route("/<ticket_id>")
@jinja.template("ticket.html")
async def show_ticket(request, ticket_id):
    ticket_db = tickets.Ticket(db=db)
    data = ticket_db.fetch_ticket(ticket_id)

    if not data:
        return {"status": 404, "code": ticket_id}

    valid_source = data["author_id"] == config["bot_id"]
    get_logs = json.loads(data["logs"])

    return {
        "status": 200, "title": f"xelA Tickets: {ticket_id}", "submitted_by": data["submitted_by"],
        "ticket_id": data["ticket_id"], "guild_id": data["guild_id"], "author_id": str(data["author_id"]),
        "created_at": datetime.fromtimestamp(data["created_at"]).strftime("%d %B %Y %H:%S"),
        "expires": datetime.fromtimestamp(data["expire"]).strftime("%d %B %Y %H:%S"), "context": data["context"],
        "channel_name": get_logs["channel_name"], "valid_source": valid_source, "logs": get_logs
    }


@app.route("/submit", methods=["POST"])
async def submit(request):
    token = request.headers.get("Authorization") or None
    post_data = request.json

    if "submitted_by" not in post_data:
        return response.json({"status": 400, "message": "Missing 'submitted_by' in JSON"}, status=400)

    if post_data["submitted_by"] == config["bot_id"]:
        if not token:
            return response.json({"status": 400, "message": "Missing Authorization headers"}, status=400)
        if token != config["token"]:
            return response.json({"status": 403, "message": "Invalid Authorization token..."}, status=403)
    else:
        return response.json({"status": 403, "message": "Anonymous post not supported yet..."}, status=403)

    make_ticket = tickets.Ticket(payload=request.json, db=db)
    code, data = make_ticket.attempt_post()

    if code != 200:
        return response.json({"status": code, "message": data.message, "validator": data.validator}, status=code)

    return response.json({"status": code, "message": data})


if __name__ == "__main__":
    # Sanic + Windows ports is weird so you can only have 1 worker on it...
    workers = 1 if os.name == "nt" else config["sanic_workers"]
    app.run(host="0.0.0.0", port=config["port"], workers=workers)
