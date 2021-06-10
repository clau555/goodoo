import subprocess
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        subprocess.run(["python", "data/main.py", sys.argv[1]])
    else:
        sys.exit("not enough arguments")
