import json
from pathlib import Path
from dataclasses import asdict
from datetime import datetime
from dice import RollResult
from stats import Session, RollEntry

base_path = Path.home() / ".dice-tracker"
def save_session(session: Session, path="session.json"):
    base_path.mkdir(exist_ok=True)
    session_path = base_path / path
    with open(session_path, 'w', encoding='utf-8') as f:
        json.dump(asdict(session), f, ensure_ascii=False, indent=4, default=str)

def load_session(path="session.json"):
    session_path = base_path / path
    if session_path.exists():
        with open(session_path) as f:
            data = json.load(f)
            entries = [
                RollEntry(
                    notation=e["notation"],
                    result=RollResult(rolls=e["result"]["rolls"], total=e["result"]["total"]),
                    timestamp=e["timestamp"]
                )
                for e in data["entries"]
            ]
            return Session(entries=entries) 
    else:
        return Session()

if __name__ == "__main__":
    from dice import parse_dice_notation, roll_dice
    from stats import add_roll

    s = Session()
    add_roll(s, roll_dice(parse_dice_notation("2d6")), "2d6")
    add_roll(s, roll_dice(parse_dice_notation("d20")), "d20")
    save_session(s)
    loaded = load_session()
    print(loaded)