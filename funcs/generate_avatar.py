import datetime
import math

from PIL import Image, ImageFont, ImageDraw

night_color = (27, 27, 54)
day_color = (1, 174, 242)

red_color = (255, 0, 0)
blue_color = (0, 212, 255)

font = ImageFont.truetype("resources/Pecita.ttf")
avatar_default = Image.open("resources/base.png")


def gradient(c_1: list[int], c_2: list[int], t: float):
    if len(c_1) != len(c_2):
        raise AttributeError()

    if t <= 0:
        return c_1
    elif t >= 1:
        return c_2
    else:
        data = []
        for i in range(len(c_1)):
            data.append(c_1[i] + (c_2[i] - c_1[i]) * t)
        return tuple(map(int, data))


def get_color_and_opacity(current_time: datetime.datetime):
    minutes = current_time.hour * 60 + current_time.minute + current_time.second / 60
    light = -math.cos((minutes - 60) / 1440 * math.pi * 2) / 2 + 0.5
    color = gradient(night_color, day_color, light) + (int((1 - light) * 0.6 * 255),)
    return color


def draw_time_clock(img: Image, current_time: datetime.datetime):
    draw = ImageDraw.Draw(img, "RGB")
    draw.text((615, 437), current_time.strftime("%H:%M"), font=font.font_variant(size=48), anchor="mm")


def draw_calendar(img: Image, current_time: datetime.datetime, temp: int):
    base = Image.new("RGBA", (125, 275), 0)
    draw = ImageDraw.Draw(base, "RGBA")

    draw.text(
        (75, 64), f"{temp}°C",
        font=font.font_variant(size=38), anchor="mm", fill=(0, 0, 0)
    )
    draw.text(
        (62, 180), f"{current_time.day}",
        font=font.font_variant(size=72), anchor="mm", fill=(0, 0, 0)
    )
    draw.text(
        (62, 230), f"{current_time.month:0>2}.{current_time.year}",
        font=font.font_variant(size=36), anchor="mm", fill=(0, 0, 0)
    )

    base = base.transform(base.size, Image.AFFINE, (1, 0, 0, 0.3, 1, 0), Image.BILINEAR)

    img.paste(base, (63, 162), base)


def get_image(current_time: datetime.datetime, temp: int):
    time_color = get_color_and_opacity(current_time)

    img = avatar_default.copy()
    base = Image.new("RGB", img.size, time_color[:3])
    draw = ImageDraw.Draw(base)
    draw.rectangle((74, 223, 94, 243), fill=gradient(blue_color, red_color, (temp+20)/60))
    base.paste(img, (0, 0), img)

    black = Image.new("RGBA", img.size, (0, 0, 0, time_color[3]))
    base.paste(black, (0, 0), black)
    draw_time_clock(base, current_time)
    draw_calendar(base, current_time, temp)

    return base
