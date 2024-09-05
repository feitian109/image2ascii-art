import numpy as np
from PIL import Image
from converter import converter
from _types import *


class core:
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
        c = converter(glyphs, font_path)

        for i in range(arr.shape[0]):
            line = ""
            for j in range(arr.shape[1]):
                line += c.color2ascii(arr[i, j].item(), linear)
            ascii_art.append(line)
        return ascii_art
