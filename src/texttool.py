from _types import *


class TextTool:
    """Text tools."""

    @staticmethod
    def save(lines: list[str], path: StrOrBytesPath):
        """
        Save lines into a txt file.

        :param lines: Lines needed to save.
        :param path: Storage location.
        """

        with open(path, "w", encoding="utf-8") as t:
            for line in lines:
                t.write(line + "\n")
