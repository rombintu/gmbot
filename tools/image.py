from PIL import Image, ImageDraw, ImageFont
from enum import Enum
import pathlib
from tools.pointer import Pointer

class Colors(Enum):
    MODE = "RGB"
    WHITE = "white"
    BLACK = "black"
    GRAY = "gray"

class Fonts(Enum):
    SPACEAGE = "Disket-Mono-Bold.ttf"

class Assets:
    background_color = Colors.WHITE.value
    color = Colors.BLACK.value
    color_mode = Colors.MODE.value
    color_shadow = Colors.GRAY.value
    font_size = 18

    def __init__(self, size_xy: int, assets_path: str):
        self.backgound_size = (size_xy, size_xy)
        self.assets_path = pathlib.Path(assets_path).absolute()
        self.p = Pointer(self.backgound_size)
        self.configure_assets()
        self.base_font = ImageFont.truetype(
            pathlib.Path(
                self.assets_path, Fonts.SPACEAGE.value
            ).as_posix(), self.font_size)
        self.lower_font = ImageFont.truetype(
            pathlib.Path(
                self.assets_path, Fonts.SPACEAGE.value
            ).as_posix(), self.font_size-6)

        self.bg_image = self.get_background_image()
        self.draw = ImageDraw.Draw(self.bg_image)

    def configure_assets(self):
        self.font_assets = pathlib.Path(self.assets_path, Fonts.SPACEAGE.value).resolve()
        self.save_path = pathlib.Path(self.assets_path, "tmp", "save.png")
        self.icons_assets = self.get_icons_png("icons-weather")

    def get_background_image(self):
        return Image.new(self.color_mode, self.backgound_size, self.background_color)
    
    def get_icons_png(self, directory: str):
        icons = {}
        icons_path = pathlib.Path(self.assets_path, directory).absolute()
        for png in icons_path.glob("*.png"):
            icons[png.name] = png.resolve()
        return icons


    def _get_icon_by_filename(self, icon_name: str):
        # sun.png
        return Image.open(
            self.icons_assets.get(icon_name)
        )
    
    def _get_icon_by_weather(self, weather: str):
        # sun
        name = weather.lower() + ".png"
        return self._get_icon_by_filename(name)
    
    def draw_icon(self, icon: Image, position: str, plus = (0, 0)):
        pos = plus
        match position:
            case "center":
                pos = self.p.to_center(icon.size, plus[0], plus[1])
            case "top":
                pos = self.p.to_top(icon.size, plus[0], plus[1])
            case "bottom":
                pos = self.p.to_bottom(icon.size, plus[0], plus[1])
            case "left":
                pos = self.p.to_left(icon.size, plus[0], plus[1])
            case "right":
                pos = self.p.to_right(icon.size, plus[0], plus[1])
        self.bg_image.paste(
            icon, pos, icon
        )


    def _draw_main_temp(self, temp: str):
        self.draw.text(
            self.p.to_center(plus_w=-35, plus_h=-25),
            temp, fill=self.color, font=self.base_font
        )
    
    def _draw_feels_temp(self, temp: str):
        self.draw.text(
            self.p.to_center(plus_w=10, plus_h=-35),
            temp, fill=self.color_shadow, font=self.lower_font
        )

    def draw_weather_temp(self, weather: str, weather_text: str, temp: str, feels_temp: str):
        icon = self._get_icon_by_weather(weather)
        self.draw_icon(icon, "center", plus=(0,-40))
        self._draw_main_temp(temp)
        self._draw_feels_temp(feels_temp)
        
        wt = '\n'.join(weather_text.split(' '))

        self.draw.text(
            self.p.to_center(plus_w=-30, plus_h=-5),
            wt, fill=self.color_shadow, font=self.lower_font
        )

    def draw_suntime(self, sunrise_time: str, sunset_time: str):
        icon_sunrise = self._get_icon_by_weather("sunrise")
        icon_sunset = self._get_icon_by_weather("sunset")
        self.draw_icon(icon_sunrise, "bottom", plus=(0, 20))
        self.draw_icon(icon_sunset, "top", plus=(0, 10))
        self.draw.text(
            self.p.to_bottom(plus_w=-20, plus_h=17),
            sunrise_time, fill=self.color_shadow, font=self.lower_font
        )
        self.draw.text(
            self.p.to_top(plus_w=-20,plus_h=-3),
            sunset_time, fill=self.color_shadow, font=self.lower_font
        )

    def draw_weather_options(self, humidity: int, wind_speed: int, cloud_percent):
        icon_humidity = self._get_icon_by_weather("wet")
        icon_wind = self._get_icon_by_weather("wind")
        icon_cloud = self._get_icon_by_weather("cloud")

        self.draw_icon(icon_humidity, "left", plus=(0, -45))
        self.draw_icon(icon_wind, "left", plus=(0, -10))
        self.draw_icon(icon_cloud, "left", plus=(0, 25))

        self.draw.text(
            self.p.to_left(plus_w=35, plus_h=-50),
            f"{humidity}%", fill=self.color_shadow, font=self.lower_font
        )
        self.draw.text(
            self.p.to_left(plus_w=35, plus_h=-17),
            f"{wind_speed}м/с", fill=self.color_shadow, font=self.lower_font
        )
        self.draw.text(
            self.p.to_left(plus_w=35, plus_h=17),
            f"{cloud_percent}%", fill=self.color_shadow, font=self.lower_font
        )

    def draw_finance(self, usd: float, eur: float, bitcoin: int):
        icon_usd = self._get_icon_by_weather("dollar")
        icon_eur = self._get_icon_by_weather("euro")
        icon_bitcoin = self._get_icon_by_weather("bitcoin")

        self.draw_icon(icon_usd, "right", plus=(0, -45))
        self.draw_icon(icon_eur, "right", plus=(0, -10))
        self.draw_icon(icon_bitcoin, "right", plus=(0, 25))

        self.draw.text(
            self.p.to_right(plus_w=-70, plus_h=-50),
            f"{usd:.2f}", fill=self.color_shadow, font=self.lower_font
        )
        self.draw.text(
            self.p.to_right(plus_w=-70, plus_h=-17),
            f"{eur:.2f}", fill=self.color_shadow, font=self.lower_font
        )
        self.draw.text(
            self.p.to_right(plus_w=-102, plus_h=17),
            f"{bitcoin:,}", fill=self.color_shadow, font=self.lower_font
        )
       