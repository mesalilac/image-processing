import argparse
import math
from PIL import Image
from tqdm import tqdm


def create_gaussian_kernel(kernel_size: int, sigma: float):
    if kernel_size % 2 == 0:
        raise ValueError("Kernel size must be odd")

    kernel = [[0.0] * kernel_size for _ in range(kernel_size)]
    offset = kernel_size // 2
    total_sum = 0.0

    for i in range(kernel_size):
        for j in range(kernel_size):
            x = j - offset
            y = i - offset

            value = (
                1 / (2 * math.pi * sigma**2) * math.exp(-(x**2 + y**2) / (2 * sigma**2))
            )

            kernel[i][j] = value
            total_sum += value

    if total_sum == 0:
        raise ValueError("Kernel sum is zero, check kernel_size and sigma")

    for i in range(kernel_size):
        for j in range(kernel_size):
            kernel[i][j] /= total_sum

    return kernel


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=False)
    parser.add_argument("--kernel-size", type=int, required=False, default=9)
    parser.add_argument("--sigma", type=float, required=False, default=5.0)

    args = parser.parse_args()
    input: str = args.input
    output: str | None = args.output
    kernel_size: int = args.kernel_size
    sigma: float = args.sigma

    if kernel_size % 2 == 0:
        raise ValueError("Kernel size must be odd")
    elif kernel_size < 3:
        raise ValueError("Kernel size must be at least 3")

    if sigma <= 0:
        raise ValueError("Sigma must be greater than zero")

    img = Image.open(input)
    new_img = Image.new(img.mode, img.size)

    print(f"------------------------------------")
    print(f"Image format: {img.format}")
    print(f"Image size: {img.size}")
    print(f"Image mode: {img.mode}")
    print(f"Kernel size: {kernel_size}")
    print(f"Sigma: {sigma}")
    print(f"------------------------------------")

    kernel = create_gaussian_kernel(kernel_size, sigma)
    kernel_sum = sum(map(sum, kernel))
    kernel_offset = kernel_size // 2

    with tqdm(
        total=img.size[0] * img.size[1], desc="Processing image", unit="px"
    ) as pbar:
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                pixel = img.getpixel((x, y))
                assert isinstance(pixel, tuple)

                r_sum = 0
                g_sum = 0
                b_sum = 0

                for i in range(kernel_size):
                    for j in range(kernel_size):
                        neighbor_x = x + (j - kernel_offset)
                        neighbor_y = y + (i - kernel_offset)

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

                pbar.update(1)

    if output is not None:
        new_img.save(output)
    else:
        new_img.show()


if __name__ == "__main__":
    main()
