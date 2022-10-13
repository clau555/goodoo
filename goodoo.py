import argparse

from src.main import main

if __name__ == "__main__":
    # getting user keyboard layout if set by user
    parser = argparse.ArgumentParser()
    parser.add_argument("keyboard_layout", type=str, default="QWERTY", nargs='?',
                        help="Defines keyboard layout, supports QWERTY and AZERTY (QWERTY by default)")
    args = parser.parse_args()

    main(args.keyboard_layout.upper())
