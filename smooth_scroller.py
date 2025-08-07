# smooth_scroller.py
# Created by John Gallaugher for use with his CircuitPython course:
# Learning videos available at: https://bit.ly/circuitpython-school
# Drag this in your CIRCUITPY/lib folder to import as a module.
# then add to code.py:
# from smooth_scroller import SmoothScroller
# See README at https://github.com/gallaugher/smooth_scroller.py for implementation details

import time
import terminalio
from adafruit_display_text.bitmap_label import Label

class SmoothScroller:
    """A smooth scrolling text label that can be added directly to display groups"""

    def __init__(self, text, display, scroll_speed=120, position=None,
                 font=None, direction="left", color=0xFFFFFF, anchor_point=None):
        self.display = display
        self.scroll_speed = scroll_speed
        self.direction = direction.lower()

        if font is None:
            font = terminalio.FONT

        if position is None:
            if self.direction in ["left", "right"]:
                position = display.height // 2
            else:
                position = display.width // 2

        if self.direction == "left":
            self.anchor_point = (0, 0.5) if anchor_point is None else anchor_point
            self.y_position = position
            self.is_horizontal = True
        elif self.direction == "right":
            self.anchor_point = (0, 0.5) if anchor_point is None else anchor_point
            self.y_position = position
            self.is_horizontal = True
        elif self.direction == "up":
            self.anchor_point = (0.5, 1) if anchor_point is None else anchor_point
            self.x_position = position
            self.is_horizontal = False
        elif self.direction in ["down", "bottom"]:
            self.anchor_point = (0.5, 0) if anchor_point is None else anchor_point
            self.x_position = position
            self.is_horizontal = False
        else:
            raise ValueError("Direction must be 'left', 'right', 'up', or 'down'")

        self.label = Label(
            font=font,
            text=text,
            color=color,
            background_tight=True,
            anchor_point=self.anchor_point,
        )

        self._setup_boundaries()
        self._reset_position()
        self.last_time = time.monotonic()

    def _setup_boundaries(self):
        bbox = self.label.bounding_box
        if self.direction == "left":
            self.label_width = bbox[2]
            self.start_pos = self.display.width
            self.end_pos = -self.label_width
        elif self.direction == "right":
            self.label_width = bbox[2]
            self.start_pos = -self.label_width
            self.end_pos = self.display.width
        elif self.direction == "up":
            self.label_height = bbox[3]
            self.start_pos = self.display.height
            self.end_pos = -self.label_height
        elif self.direction == "down":
            self.label_height = bbox[3]
            self.start_pos = -self.label_height
            self.end_pos = self.display.height

    def _reset_position(self):
        self.current_pos = self.start_pos
        if self.is_horizontal:
            self.label.anchored_position = (int(self.current_pos), self.y_position)
        else:
            self.label.anchored_position = (self.x_position, int(self.current_pos))

    def update(self):
        now = time.monotonic()
        elapsed = now - self.last_time
        self.last_time = now

        if self.direction in ["left", "up"]:
            self.current_pos -= self.scroll_speed * elapsed
            if self.current_pos < self.end_pos:
                self.current_pos = self.start_pos
        else:
            self.current_pos += self.scroll_speed * elapsed
            if self.current_pos > self.end_pos:
                self.current_pos = self.start_pos

        if self.is_horizontal:
            self.label.anchored_position = (int(self.current_pos), self.y_position)
        else:
            self.label.anchored_position = (self.x_position, int(self.current_pos))

    def set_text(self, new_text):
        self.label.text = new_text
        self._setup_boundaries()

    def set_speed(self, new_speed):
        self.scroll_speed = new_speed

    def reset(self):
        self._reset_position()

    def __getattr__(self, name):
        return getattr(self.label, name)
