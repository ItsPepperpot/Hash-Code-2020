import sys


def main(filename):
    """Main function."""

    if not filename:
        filename = input("Please enter a filename:\n")

    with open(filename) as f:
        # 1. parse input
        f.write()

    # 2. do something with input

    with open(filename.replace("", ""), "w") as f:
        # 3. write output
        f.write()


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except:
        main(None)
