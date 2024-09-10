from _types import *


class TextTool:
    """Text tools."""

    @staticmethod
    def read(path: StrOrBytesPath) -> list[str]:
        """
        From a txt file read lines.

        :param path: txt file location.
        """
        with open(path, "r", encoding="utf-8") as t:
            return t.readlines()

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
