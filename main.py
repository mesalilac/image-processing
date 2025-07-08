import argparse
from PIL import Image


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)

    args = parser.parse_args()
    input = args.input
    output = args.output

    img = Image.open(input)

    print(img)


if __name__ == "__main__":
    main()
