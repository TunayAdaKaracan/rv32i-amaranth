import argparse
from tests.run_tests import run_tests


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparser = parser.add_subparsers(dest="command")
    tests = subparser.add_parser("tests")
    tests.add_argument("-t", "--test", choices=["alu"])
    tests.add_argument("-c", "--clear", action="store_true")
    args = parser.parse_args()
    
    if args.command is None:
        # TODO: Upload code
        pass
    elif args.command == "tests":
        run_tests(args.test, args.clear)

if __name__ == "__main__":
    main()