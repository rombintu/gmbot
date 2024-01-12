import os
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError

from  internal import logger

WORK_DIR = os.getcwd()
TMP_DIR = os.path.join(WORK_DIR, "tmp")
ASSETS_DIR = os.path.join(WORK_DIR, "assets")
PATTERN_NAME = "pattern.jpg"
# FONT_NAME = "spaceage.ttf"
# FONT_NAME = "modern_space.otf"
FONT_NAME = "Disket-Mono-Regular.ttf"
OUTPUT_NAME = "image.jpg"
MODE_L = "L"

class Text:
    color = (255,255,255) # White
    origin = (0,0)
    def __init__(self, text: str):
        self.w, self.h = 32, 32
        self.text = text
        self.xy = (100, 100)
        self.load_font()

    def load_font(self):
        try:
            self.font = ImageFont.truetype(os.path.join(ASSETS_DIR, FONT_NAME), 32)
        except Exception as err:
            logger.warning(err)
            self.font = ImageFont.load_default(128)

def draw(text: Text):
    pattern_img = None
    try:
        pattern_img = Image.open(os.path.join(ASSETS_DIR, PATTERN_NAME))
    except UnidentifiedImageError as err:
        logger.error(err)
        # TODO
    except Exception as err:
        logger.error(err)

    pattern_obj = ImageDraw.Draw(pattern_img)
    pattern_obj.text(text.xy, text.text, font=text.font, fill=text.color, spacing=0, align="left")
    pattern_img.save(os.path.join(TMP_DIR, OUTPUT_NAME))
