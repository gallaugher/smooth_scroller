# SmoothScroller — A Flexible Text Scroller for CircuitPython

A lightweight, reusable CircuitPython class for creating smooth scrolling labels on displays using `displayio`. Supports all directions: **left**, **right**, **up**, and **down**.

## 📽 Demo

[![Watch the video](https://user-images.githubusercontent.com/123456789/your-image.png)](https://youtu.be/-lrJ0fy0xm0?si=9HCbgmnwOycmiC4h)

▶️ [YouTube Lesson:] Coming Soon.

## 📦 Installation

1. Copy `smooth_scroller.py` to your `CIRCUITPY/lib/` directory.
2. Make sure you also have `adafruit_display_text` and `adafruit_bitmap_font` in `lib`.

## ✅ Example Usage

```python
from smooth_scroller import SmoothScroller
from adafruit_display_text.bitmap_label import Label
from adafruit_bitmap_font import bitmap_font
import board, displayio

# Set up your display...
# display = ...

font = bitmap_font.load_font("/fonts/helvB08.bdf")

scroller = SmoothScroller(
    text="Hack the Planet!",
    display=display,
    font=font,
    scroll_speed=100,
    direction="right",  # or "left", "up", "down"
    color=0x00FF00,
)

display.root_group.append(scroller.label)

while True:
    scroller.update()
