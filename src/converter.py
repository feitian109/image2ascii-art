import numpy as np
from PIL import Image, ImageFont, ImageDraw

from _types import *
from fonttool import FontTool


class Converter:
    """Convert color value to ascii character."""

    # `c2a` stands for color_to_ascii

    def __init__(self, glyphs: list[str], font_path: StrOrBytesPath):
        self._c2a_base = self._get_c2a(glyphs, font_path)
        self._c2a_items = self._get_sorted_item(self._c2a_base)
        self._c2a_filled = {}
        self._c2a_linear = {}

    @staticmethod
    def _get_c2a(glyphs: list[str], font_path: StrOrBytesPath) -> dict[int, str]:
        font = ImageFont.truetype(font_path, 72)
        # determine canvas size
        _, _, max_right, max_btm = FontTool.get_fontbbox(font)
        color_value = []

        # get every glyph's color value
        for glyph in glyphs:
            glyph_img = Image.new("L", (int(max_right), int(max_btm)), color=255)
            draw = ImageDraw.Draw(glyph_img)
            draw.text((0, 0), glyph, fill=0, font=font)
            color_value.append(np.array(glyph_img).sum())

        # convert value into [0, 255]
        color_value -= min(color_value)
        max_value = max(color_value)
        for i, value in enumerate(color_value):
            color_value[i] = round(value / (max_value / 255))

        return dict(zip(color_value, glyphs))

    @staticmethod
    def _get_sorted_item(c2a_dict: dict[int, str]) -> list:
        """Make c2a easy to print and iter"""
        return sorted(c2a_dict.items(), key=lambda x: x[0])

    @staticmethod
    def _fill_dict(c2a_dict: dict[int, str]) -> dict[int, str]:
        """Extend c2a_dict for any color in the range of [0,255]"""
        dic = {}

        for i in range(0, 255):
            closest = min(c2a_dict.keys(), key=lambda x: abs(x - i))
            dic[i] = c2a_dict[closest]
        return dic

    def _init_c2a_filled(self):
        print(f"Color2Ascii: {self._c2a_items}")
        self._c2a_filled = self._fill_dict(self._c2a_base)

    def _init_c2a_linear(self):
        step = 255 / (len(self._c2a_base) - 1)
        for i, (_, ascii_code) in enumerate(self._c2a_items):
            self._c2a_linear[round(i * step)] = ascii_code
        print(f"Color2Ascii (Linear): {self._get_sorted_item(self._c2a_linear)}")
        self._c2a_linear = self._fill_dict(self._c2a_linear)

    def color2ascii(self, value: int, linear: bool = False) -> str:
        """
        Convert color value to ascii character.

        :param value: Color value.
        :param linear: Enable linear mode. This will make output more smooth.
        """

        if linear:
            if not self._c2a_linear:
                self._init_c2a_linear()
            return self._c2a_linear[value]

        else:
            if not self._c2a_filled:
                self._init_c2a_filled()
            return self._c2a_filled[value]
