import sys


def parse_args():
    if len(sys.argv) >1 :
        for v in sys.argv[1:]:
            print(v)

if __name__ == "__main__":
    parse_args()