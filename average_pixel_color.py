import argparse
from PIL import Image
from tqdm import trange


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=False)

    args = parser.parse_args()
    input = args.input
    output = args.output

    img = Image.open(input)
    print(f"Image format: {img.format}")
    print(f"Image size: {img.size}")
    print(f"Image mode: {img.mode}")

    sum_r = 0
    sum_g = 0
    sum_b = 0

    for pixel in list(img.getdata()):
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]

        sum_r += r
        sum_g += g
        sum_b += b

    total_pixels = img.size[0] * img.size[1]

    average_r = round(sum_r / total_pixels)
    average_g = round(sum_g / total_pixels)
    average_b = round(sum_b / total_pixels)

    print(f"Average pixel color: rgb({average_r}, {average_g}, {average_b})")

    new_img = Image.new(img.mode, img.size)
    for x in trange(img.size[0]):
        for y in range(img.size[1]):
            new_img.putpixel((x, y), (average_r, average_g, average_b))

    if output is not None:
        new_img.save(output)
    else:
        new_img.show()


if __name__ == "__main__":
    main()
