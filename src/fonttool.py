import string

from PIL import ImageFont

ASCII_GLYPHS = list(string.ascii_letters + string.digits + string.punctuation + " ")


class FontTool:
    """A collection of font tool."""

    @staticmethod
    def get_fontbbox(
            font: ImageFont.FreeTypeFont, glyphs: list[str] | None = None
    ) -> tuple[float, float, float, float]:
        """
        Get font's bound box. Return a tuple contain `min_left`, `min_top`, `max_right`, `max_btm`

        :param font: `ImageFont.FreeTypeFont`
        :param glyphs: Glyphs used to calculate font's bound box.
        """

        if glyphs is None:
            glyphs = ASCII_GLYPHS

        min_left, min_top, max_right, max_btm = font.getbbox(glyphs[0])
        for glyph in glyphs:
            left, top, right, btm = font.getbbox(glyph)
            min_left = min(left, min_left)
            min_top = min(top, min_top)
            max_right = max(right, max_right)
            max_btm = max(btm, max_btm)
        return min_left, min_top, max_right, max_btm
