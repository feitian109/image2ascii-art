import bisect
import numpy as np
from PIL import Image, ImageFont, ImageDraw

from _types import StrOrBytesPath
from font_tool import FontTool


class Converter:
    """Convert color value to ascii character."""

    # `c2a` stands for color_to_ascii
    def __init__(self, glyphs: list[str], font_path: StrOrBytesPath):
        color_values = self.__get_color_value(glyphs, font_path)

        # sort `color_values` and `glyphs`
        bundles = list(zip(color_values, glyphs))
        bundles = sorted(bundles, key=lambda x: x[0])

        self.color_values = [i[0] for i in bundles]
        self.glyphs = [i[1] for i in bundles]

    @staticmethod
    def __get_color_value(glyphs: list[str], font_path: StrOrBytesPath) -> list[int]:
        font = ImageFont.truetype(font_path, 72)
        # determine canvas size
        _, _, max_right, max_btm = FontTool.getfontbbox(font)
        color_value = []  # type: list[int]

        # get every glyph's color value
        for glyph in glyphs:
            glyph_img = Image.new("L", (int(max_right), int(max_btm)), color=255)
            draw = ImageDraw.Draw(glyph_img)
            draw.text((0, 0), glyph, fill=0, font=font)
            color_value.append(np.array(glyph_img).sum())

        # convert value into [0, 255]
        min_color_value = min(color_value)
        color_value = [i - min_color_value for i in color_value]
        max_value = max(color_value)
        for i, value in enumerate(color_value):
            color_value[i] = round(value / (max_value / 255))
        return color_value

    @staticmethod
    def __fill_c2a(c2a_dict: dict[int, str]) -> dict[int, str]:
        """Extend c2a_dict for any color in the range of [0,255]"""
        dic = {}
        c2a_dict_keys = list(c2a_dict.keys())

        for i in range(0, 255):
            idx = bisect.bisect(c2a_dict_keys, i)
            idx_of_better_key = min(
                idx - 1, idx, key=lambda idx: abs(c2a_dict_keys[idx] - i)
            )
            dic[i] = c2a_dict[c2a_dict_keys[idx_of_better_key]]

        return dic

    def __get_c2a_linear(self):
        c2a_linear = {}

        step = 255 / (len(self.glyphs) - 1)
        for i, glyph in enumerate(self.glyphs):
            c2a_linear[round(i * step)] = glyph
        return c2a_linear

    def color2ascii(self, linear: bool = False) -> dict[int, str]:
        """
        Return a dict mapping color to glyph.

        :param linear: Enable linear mode. This will make output more smooth.
        """

        if linear:
            c2a = self.__get_c2a_linear()
        else:
            c2a = dict(zip(self.color_values, self.glyphs))

        print(f"Color2Ascii: {c2a}")
        return self.__fill_c2a(c2a)

    def ascii2color(self) -> dict[str, int]:
        """
        Return a dict mapping glyph to color.
        """
        return dict(zip(self.glyphs, self.color_values))
