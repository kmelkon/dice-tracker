from dataclasses import dataclass
import re
import random

@dataclass
class DiceRoll:
    count: int
    sides: int
    modifier: int = 0

@dataclass
class RollResult:
    rolls: list[int]
    total: int

def parse_dice_notation(notation: str) -> DiceRoll:
    pattern = r'^(\d*)d(\d+)([+-]\d+)?$'
    match = re.match(pattern, notation)
    if not match:
        raise ValueError(f"Invalid dice notation: {notation}")
    count = int(match.group(1)) if match.group(1) else 1
    sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    if sides < 1:
        raise ValueError(f"Invalid number of sides: {sides}")
    if count < 1:
        raise ValueError(f"Invalid count: {count}")
    return DiceRoll(count=count, sides=sides, modifier=modifier)

def roll_dice(dice_roll: DiceRoll) -> RollResult:
    rolls = [random.randint(1, dice_roll.sides) for _ in range(dice_roll.count)]
    return RollResult( 
        rolls=rolls,
        total=sum(rolls) + dice_roll.modifier
    )