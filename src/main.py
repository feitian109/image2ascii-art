from pathlib import Path
from PIL import Image
from image_tool import image_tool
from core import core
from render import render
from text_tool import text_tool


def minimal_demo(
    input_path: Path, glyphs: list[str], font_path: Path, output_path: Path
):
    processed_img = image_tool.preprocess(Image.open(input_path))
    ascii_text = core.asciify(processed_img, glyphs, font_path)
    r = render(font_path)
    ascii_img = r.rend(ascii_text, margin=-1)
    ascii_img.save(output_path / f"{input_path.stem}_ascii.png")
    text_tool.save(ascii_text, output_path / f"{input_path.stem}_ascii.txt")


# You can custom your glyphs here
simple_glyphs = list(r" .1257:BDEIJKLMPQRSUXYZbdgijqrsuv")
more_glyphs = list(
    r" 0123456789!#%&*+,-./:;<=>?@\|~abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
)

# input
input_path = Path(r"./examples/input/vegetables.png")

# About font, you can read this doc `assets/README.md`
font_path = Path(r"./assets/fonts/FiraMono.ttf")

# output
output_path = Path(r"./examples/output")

# Run our demo
minimal_demo(input_path, more_glyphs, font_path, output_path)
print("Done")
