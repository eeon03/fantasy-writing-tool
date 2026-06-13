import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from datetime import datetime

SESSION_FILE = "data/session.json"
MAX_SPARKS = 5


def _load_session():
    if not os.path.exists(SESSION_FILE):
        return _fresh_session()
    with open(SESSION_FILE, "r") as f:
        return json.load(f)


def _save_session(session):
    os.makedirs("data", exist_ok=True)
    with open(SESSION_FILE, "w") as f:
        json.dump(session, f, indent=2)


def _fresh_session():
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "started": datetime.now().strftime("%H:%M"),
        "sparks_used": 0,
        "sparks_remaining": MAX_SPARKS,
        "locked": False
    }


def start_session():
    session = _load_session()
    today = datetime.now().strftime("%Y-%m-%d")

    if session.get("date") != today:
        session = _fresh_session()
        _save_session(session)
        print(f"\n  New session started. {MAX_SPARKS} sparks available.")
    else:
        remaining = session.get("sparks_remaining", 0)
        if session.get("locked"):
            print(f"\n  Session locked — all {MAX_SPARKS} sparks used today.")
            print("  Come back tomorrow or write without the AI.")
        else:
            print(f"\n  Session active. {remaining} sparks remaining today.")

    return session


def use_spark():
    session = _load_session()

    if session.get("locked"):
        return False, 0

    session["sparks_used"] += 1
    session["sparks_remaining"] -= 1

    if session["sparks_remaining"] <= 0:
        session["sparks_remaining"] = 0
        session["locked"] = True

    _save_session(session)
    return True, session["sparks_remaining"]


def sparks_remaining():
    session = _load_session()
    return session.get("sparks_remaining", 0)


def is_locked():
    session = _load_session()
    today = datetime.now().strftime("%Y-%m-%d")
    if session.get("date") != today:
        return False
    return session.get("locked", False)


def session_status():
    session = _load_session()
    today = datetime.now().strftime("%Y-%m-%d")

    if session.get("date") != today:
        print(f"\n  No session today yet. {MAX_SPARKS} sparks available.")
        return

    print(f"\n  --- Session Status ---")
    print(f"  Date: {session.get('date')}")
    print(f"  Started: {session.get('started')}")
    print(f"  Sparks used: {session.get('sparks_used')}/{MAX_SPARKS}")
    print(f"  Sparks remaining: {session.get('sparks_remaining')}")
    if session.get("locked"):
        print("  Status: LOCKED — come back tomorrow")
    else:
        print("  Status: active")