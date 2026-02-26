from dataclasses import dataclass, field
from datetime import datetime

from dice import RollResult, parse_dice_notation, roll_dice
import statistics
from collections import Counter

@dataclass
class RollEntry:
    notation: str
    result: RollResult
    timestamp: datetime

@dataclass
class Session:
    entries: list[RollEntry] = field(default_factory=list)

@dataclass
class MostCommonRoll:
    roll_result: int
    roll_count: int

@dataclass
class History:
    mean: float
    median: float
    stdev: float | None
    min_roll: int
    max_roll: int
    most_common_roll: MostCommonRoll
        
    

def add_roll(session: Session, result: RollResult, notation: str) -> None:
    session.entries.append(RollEntry(notation=notation, timestamp=datetime.now(),result=result))

def get_stats(session: Session, notation: str | None = None) -> History:
    if len(session.entries) == 0:
        raise ValueError("Session contains no entries.")
    
    entries = [e for e in session.entries if e.notation == notation] if notation else session.entries
    
    if len(entries) == 0:
        raise ValueError(f"Notation filter contains no entries: {notation}")
    
    totals = [entry.result.total for entry in entries]
    mean = statistics.mean(totals)
    median = statistics.median(totals)
    standard_deviation = statistics.stdev(totals) if len(totals) >= 2 else None
    min_roll = min(totals)
    max_roll = max(totals)
    c = Counter(totals)
    most_common = c.most_common(1)

    return History(
        mean=mean,
        median=median,
        stdev=standard_deviation,
        min_roll=min_roll,
        max_roll=max_roll,
        most_common_roll=MostCommonRoll(
            roll_result=most_common[0][0],
            roll_count=most_common[0][1]
        )
    )

if __name__ == "__main__":
    s = Session()
    add_roll(s,roll_dice(parse_dice_notation("2d6")), "2d6")
    add_roll(s,roll_dice(parse_dice_notation("2d6")), "2d6")
    add_roll(s,roll_dice(parse_dice_notation("2d6")), "2d6")
    add_roll(s,roll_dice(parse_dice_notation("2d20")), "2d20")
    add_roll(s,roll_dice(parse_dice_notation("d4")), "d4")
    print(get_stats(s))