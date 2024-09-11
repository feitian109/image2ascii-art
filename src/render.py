from PIL import Image, ImageDraw, ImageFont

from _types import *
from fonttool import FontTool


class Render:
    """Text render for image generate."""

    def __init__(self, font_path: StrOrBytesPath, font_size: float = 12):
        self.font = ImageFont.truetype(font_path, font_size)

        # get font's bound box
        min_left, _, max_right, max_btm = FontTool.get_fontbbox(self.font)
        self.width = max_right - min_left
        self.height = max_btm

    def rend(
        self,
        lines: list[str],
        padding_offset: float = 0,
        margin: float = 0,
        text_color: tuple[int, int, int, int] = (0, 0, 0, 255),
        background_color: tuple[int, int, int, int] = (255, 255, 255, 255),
    ) -> Image.Image:
        """
        Main function for text rending. Return a `PIL Image` object (in RGBA color mode).

        :param lines: Lines needed to rend.
        :param padding_offset: Sum an offset to default padding. Default is `0`.
        :param margin: Margin wraps a character. Default is `0`.
        :param text_color: Default is black `(0, 0, 0, 255)`.
        :param background_color: Default is white `(255, 255, 255, 255)`.
        """

        padding = (self.height - self.width) / 2 + padding_offset
        assert padding > 0

        block_width = self.width + (padding + margin) * 2
        block_height = self.height + margin * 2

        # image_size = (image_width, image_height)
        image_size = (int(block_width * len(lines[0])), int(block_height * len(lines)))
        print(f"Rended image size: {image_size[0]}x{image_size[1]}")

        img = Image.new("RGBA", image_size, color=background_color)
        draw = ImageDraw.Draw(img)

        # init position
        x = margin + padding
        y = margin

        for line in lines:
            for glyph in line:
                draw.text((x, y), glyph, fill=text_color, font=self.font)
                x += self.width + (padding + margin) * 2
            x = margin + padding
            y += self.height + margin * 2

        return img
