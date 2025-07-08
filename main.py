import argparse
from PIL import Image
from tqdm import trange


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=False, default="output.png")

    args = parser.parse_args()
    input = args.input
    output = args.output

    img = Image.open(input)
    new_img = Image.new(img.mode, img.size)
    print(f"Image format: {img.format}")
    print(f"Image size: {img.size}")
    print(f"Image mode: {img.mode}")

    kernel = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ]
    kernel_sum = sum(map(sum, kernel))

    kernel_width = len(kernel[0])
    kernel_height = len(kernel)
    kernel_offset_x = round(kernel_width / 2)
    kernel_offset_y = round(kernel_height / 2)

    for x in trange(img.size[0]):
        for y in range(img.size[1]):
            pixel = img.getpixel((x, y))
            assert isinstance(pixel, tuple)

            r_sum = 0
            g_sum = 0
            b_sum = 0

            for i in range(kernel_height):
                for j in range(kernel_width):
                    neighbor_x = x + (j - kernel_offset_x)
                    neighbor_y = y + (i - kernel_offset_y)

                    kx: int = max(0, min(neighbor_x, img.size[0] - 1))
                    ky: int = max(0, min(neighbor_y, img.size[1] - 1))

                    neighbor_pixel = img.getpixel((kx, ky))

                    if isinstance(neighbor_pixel, tuple):
                        r_sum += kernel[i][j] * neighbor_pixel[0]
                        g_sum += kernel[i][j] * neighbor_pixel[1]
                        b_sum += kernel[i][j] * neighbor_pixel[2]

            new_r = round(r_sum / kernel_sum)
            new_g = round(g_sum / kernel_sum)
            new_b = round(b_sum / kernel_sum)

            new_img.putpixel((x, y), (new_r, new_g, new_b))

    new_img.show()
    # new_img.save(output)


if __name__ == "__main__":
    main()
