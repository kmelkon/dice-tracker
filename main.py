import argparse

from dice import parse_dice_notation, roll_dice
from stats import History, Session, add_roll, get_stats
from storage import load_session, save_session

def print_history(history: History):
    print(f"Mean: {history.mean}")
    print(f"Median: {history.median}")
    print(f"Standard deviation: {history.stdev}")
    print(f"Minimum roll: {history.min_roll}")
    print(f"Maximum roll: {history.max_roll}")
    print(f"Most common roll result: {history.most_common_roll.roll_result}")
    print(f"Most common roll count: {history.most_common_roll.roll_count}")
    

def main():
    parser = argparse.ArgumentParser(description="Dice Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # "roll" subcommand
    roll_parser = subparsers.add_parser("roll")
    roll_parser.add_argument("notation", type=str)
    roll_parser.add_argument("--times", type=int, default=1)

    # "stats" subcommand
    stats_parser = subparsers.add_parser("stats")
    stats_parser.add_argument("--notation", type=str, default=None)

    args = parser.parse_args()

    # args.command → "roll" or "stats"
    session = load_session()
    match args.command:
        case "roll":
        # on each successful roll add_roll from stats.py
            for _ in range(args.times):
                roll_result = roll_dice(parse_dice_notation(args.notation))
                print(f"You rolled {args.notation} and got: {roll_result.rolls}")
                print(f"You roll total is: {roll_result.total}")
                add_roll(
                    session,
                    roll_result,
                    args.notation
                    )
                save_session(session)
        case "stats":
            if args.notation:
                history = get_stats(session, args.notation)
            else:
                history = get_stats(session)
            print_history(history)
        case _:
            raise ValueError("You need to pass either a roll or stats subcommand")
 
if __name__ == "__main__":
    main()