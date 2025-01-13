# cli.py
import argparse
from xtime import xsleep, XSleep

def main():
    parser = argparse.ArgumentParser(description="Command-line utility for XTime.", prog="xtime")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Sleep command
    sleep_parser = subparsers.add_parser("sleep", help="Sleep for a specified amount of time.")
    sleep_parser.add_argument("time", type=float, help="Time to sleep in seconds.")

    # Add subparsers for different units
    unit_subparsers = sleep_parser.add_subparsers(dest="unit", help="Unit of time")

    # Seconds
    seconds_parser = unit_subparsers.add_parser("seconds", help="Sleep for a specified number of seconds")
    seconds_parser.add_argument("value", type=float, help="Time to sleep in seconds")

    # Milliseconds
    milliseconds_parser = unit_subparsers.add_parser("milliseconds", help="Sleep for a specified number of milliseconds")
    milliseconds_parser.add_argument("value", type=float, help="Time to sleep in milliseconds")

    # Minutes
    minutes_parser = unit_subparsers.add_parser("minutes", help="Sleep for a specified number of minutes")
    minutes_parser.add_argument("value", type=float, help="Time to sleep in minutes")

    # Hours
    hours_parser = unit_subparsers.add_parser("hours", help="Sleep for a specified number of hours")
    hours_parser.add_argument("value", type=float, help="Time to sleep in hours")

    # Command for additional functions
    func_parser = subparsers.add_parser("func", help="Executes additional XSleep functions.")
    func_parser.add_argument("fname", choices=[
        "get_pid", "get_cpu_count", "get_random_delay", "is_interactive",
        "get_platform", "get_uptime", "get_free_memory", "get_username",
        "get_current_time_ms", "execute_command", "print_message_with_delay"
    ], help="Name of the function to execute.")
    func_parser.add_argument("args", nargs="*", help="Arguments for the function (if any).")

    args = parser.parse_args()

    if args.command == "sleep":
        if args.unit == "seconds":
            xsleep(args.value)
        elif args.unit == "milliseconds":
            xs = XSleep()
            xs.milliseconds(args.value)
        elif args.unit == "minutes":
            xs = XSleep()
            xs.minutes(args.value)
        elif args.unit == "hours":
            xs = XSleep()
            xs.hours(args.value)
        else:  # Default to seconds if no unit is specified
            xsleep(args.time)
    elif args.command == "func":
        xs = XSleep()
        func = getattr(xs, args.fname)
        if args.fname == "get_random_delay":
            if len(args.args) != 2:
                print("Error: get_random_delay needs 2 arguments (min_seconds, max_seconds).")
                return
            min_secs = float(args.args[0])
            max_secs = float(args.args[1])
            func(min_secs, max_secs)
        elif args.fname == "execute_command":
            if not args.args:
                print("Error: execute_command needs at least 1 argument (command).")
                return
            command = " ".join(args.args)
            result = func(command)
            print(result)
        elif args.fname == "print_message_with_delay":
            if len(args.args) < 2:
                print("Error: print_message_with_delay needs at least 2 arguments (message, delay_seconds).")
                return
            message = args.args[0]
            delay_seconds = float(args.args[1])
            func(message, delay_seconds)
        else:
            result = func(*args.args)
            if result is not None:
                print(result)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()