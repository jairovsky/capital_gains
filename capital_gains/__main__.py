from capital_gains.cli import run
import sys

if __name__ == '__main__':
    sys.stdout.writelines(run(sys.stdin))