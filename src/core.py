import numpy as np
from PIL import Image

from _types import *
from converter import Converter


class Core:
    """Core functions convert image to ascii-art."""

    @staticmethod
    def asciify(
            image: Image.Image,
            glyphs: list[str],
            font_path: StrOrBytesPath,
            linear: bool = False,
    ) -> list[str]:
        """
        Convert `PIL Image` object to `ascii_art`.

        :param image: `PIL Image` object.
        :param glyphs: A `list` contains glyphs that will be used to generate `ascii_art`.
        :param font_path: The converter will optimize the output according to different fonts.
        :param linear: Enable linear mode. This will make output more smooth. Default is `False`.
        """

        arr = np.array(image)
        ascii_art = []
        c = Converter(glyphs, font_path)
        color2ascii = c.color2ascii(linear=linear)

        for i in range(arr.shape[0]):
            line = ""
            for j in range(arr.shape[1]):
                line += color2ascii[arr[i, j].item()]
            ascii_art.append(line)
        return ascii_art

    @staticmethod
    def unasciify(
            lines: list[str],
            font_path: StrOrBytesPath,
    ) -> Image.Image:
        """
        Convert `ascii_art` back to `PIL Image` object.

        :param lines: `ascii_art` needs to convert back.
        :param font_path: `unasciify` use a font file to get a dict describing how to convert ascii to color.
        """

        glyphs = set()
        for line in lines:
            for glyph in line:
                glyphs.add(glyph)

        c = Converter(list(glyphs), font_path)
        ascii2color = c.ascii2color()

        image_width = len(lines[0]) - 1  # remove '\n' at the end of line
        image_height = len(lines)
        arr = np.empty([image_height, image_width], dtype=np.uint8)

        print(f"Output image size: {image_width}x{image_height}")
        for i in range(image_height):
            for j in range(image_width):
                arr[i, j] = ascii2color[lines[i][j]]

        return Image.fromarray(arr)
