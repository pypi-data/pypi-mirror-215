from typing import Optional
from .point import Point
from .segment import Segment
import numpy as np


class BoundingBox:
    """
    A bounding box is a rectangle that has a left, top, right, and bottom.
    The coordinates of a box are meant to be normalized pdf coordinates i.e.
    the origin is at the bottom left of the page, the x-axis is horizontal and increases
    to the right, and the y-axis is vertical and increases upwards and the page coordinates
    is left = 0, top = 1, right = 1, bottom = 0.
    """

    def __init__(self, left: float, top: float, right: float, bottom: float):
        self.left = float(left)
        self.top = float(top)
        self.right = float(right)
        self.bottom = float(bottom)
        self.height = self.top - self.bottom
        self.width = self.right - self.left
        self.validate_args()

    def validate_args(self):
        """Validate the arguments of the bounding box."""
        if self.right <= self.left:
            raise ValueError("right must be greater than left")
        if self.top <= self.bottom:
            raise ValueError("top must be greater than bottom")

    def get_left(self) -> float:
        """Get the left coordinate of the bounding box."""
        return self.left

    def get_top(self) -> float:
        """Get the top coordinate of the bounding box."""
        return self.top

    def get_right(self) -> float:
        """Get the right coordinate of the bounding box."""
        return self.right

    def get_bottom(self) -> float:
        """Get the bottom coordinate of the bounding box."""
        return self.bottom

    def get_width(self) -> float:
        """Get the width of the bounding box."""
        return self.right - self.left

    def get_area(self) -> float:
        """Get the area of the bounding box."""
        return self.get_width() * self.get_height()

    def get_height(self) -> float:
        """Get the height of the bounding box."""
        return self.top - self.bottom

    def get_center(self) -> Point:
        """Get the center of the bounding box."""
        center_x = (self.left + self.right) / 2
        center_y = (self.top + self.bottom) / 2
        return Point(center_x, center_y)

    def get_top_left(self) -> Point:
        """Get the top left point of the bounding box."""
        return Point(self.left, self.top)

    def get_top_right(self) -> Point:
        """Get the top right point of the bounding box."""
        return Point(self.right, self.top)

    def get_bottom_left(self) -> Point:
        """Get the bottom left point of the bounding box."""
        return Point(self.left, self.bottom)

    def get_bottom_right(self) -> Point:
        """Get the bottom right point of the bounding box."""
        return Point(self.right, self.bottom)

    def get_horizontal_segment(self):
        """Get the horizontal segment of the bounding box."""
        return Segment(self.left, self.right)

    def get_vertical_segment(self):
        """Get the vertical segment of the bounding box."""
        return Segment(self.bottom, self.top)

    def scale(
        self,
        width_scale: float = 1,
        height_scale: float = 1,
        width_offset: float = 0,
        height_offset: float = 0,
    ) -> "BoundingBox":
        if width_scale <= 0 or height_scale <= 0:
            raise ValueError("scale must be greater than 0")
        if width_offset < 0 or height_offset < 0:
            raise ValueError("offset must be greater than or equal to 0")
        center = self.get_center()
        hor_shift = self.width * width_scale / 2 + width_offset / 2
        ver_shift = self.height * (height_scale / 2) + height_offset / 2
        left = center.x - hor_shift
        top = center.y + ver_shift
        right = center.x + hor_shift
        bottom = center.y - ver_shift
        return BoundingBox(left, top, right, bottom)

    def translate(self, x: float, y: float) -> "BoundingBox":
        """Translate the bounding box by x in the horizontal axis and by y in the vertical axis."""
        return BoundingBox(self.left + x, self.top + y, self.right + x, self.bottom + y)

    def horizontal_intersect(self, other: "BoundingBox") -> bool:
        """Check if the bounding boxes intersect horizontally."""
        return self.left <= other.right and other.left <= self.right

    def vertical_intersect(self, other: "BoundingBox") -> bool:
        """Check if the bounding boxes intersect vertically."""
        return self.bottom <= other.top and other.bottom <= self.top

    def intersect(self, other: "BoundingBox") -> bool:
        """Check if the bounding boxes intersect."""
        return self.horizontal_intersect(other) and self.vertical_intersect(other)

    def contains_point(self, point: Point) -> bool:
        """Check if the bounding box contains the point."""
        return (
            self.left <= point.x
            and self.right >= point.x
            and self.bottom <= point.y
            and self.top >= point.y
        )

    def __le__(self, other):
        """Check if the bounding box is weakly inside the other bounding box."""
        return (
            self.left >= other.left
            and self.right <= other.right
            and self.top <= other.top
            and self.bottom >= other.bottom
        )

    def __lt__(self, other):
        """Check if the bounding box is strongly inside the other bounding box."""
        return (
            self.left > other.left
            and self.right < other.right
            and self.top < other.top
            and self.bottom > other.bottom
        )

    def __str__(self):
        return (
            f"BoundingBox(l={self.left:.3g}, t={self.top:.3g}, "
            f"r={self.right:.3g}, b={self.bottom:.3g})"
        )

    def __repr__(self):
        return str(self)

    @staticmethod
    def compose_bounding_boxes(
        bounding_boxes: list["BoundingBox"],
    ) -> Optional["BoundingBox"]:
        """Compose a list of bounding boxes into a single bounding box.
        The resulting bounding box is the smallest bounding box that contains all
        the bounding boxes in the list.
        """
        if not bounding_boxes:
            return None
        left = min(bounding_boxes, key=lambda bb: bb.left).left
        top = max(bounding_boxes, key=lambda bb: bb.top).top
        right = max(bounding_boxes, key=lambda bb: bb.right).right
        bottom = min(bounding_boxes, key=lambda bb: bb.bottom).bottom
        return BoundingBox(left, top, right, bottom)

    @staticmethod
    def split_bounding_box(
        bounding_box: "BoundingBox",
        num_boxes: int,
        weights: np.ndarray = None,
    ) -> list["BoundingBox"]:
        """Split a bounding box into a list of bounding boxes.
        The bounding boxes are split evenly along the width of the bounding box."""
        if num_boxes < 1:
            raise ValueError("num_boxes must be greater than 0")
        if weights is not None and len(weights) != num_boxes:
            raise ValueError("weights must be the same length as num_boxes")

        if num_boxes == 1:
            return [bounding_box]

        if weights is None:
            weights = np.full(num_boxes, 1 / num_boxes)
        else:
            total_weight = sum(weights)
            weights = weights / total_weight

        width = bounding_box.get_width()
        left = bounding_box.left
        top = bounding_box.top
        bottom = bounding_box.bottom
        char_widths = weights * width
        bounding_boxes = []
        char_left = left
        for i in range(num_boxes):
            char_right = char_left + char_widths[i]
            bounding_boxes.append(
                BoundingBox(
                    char_left,
                    top,
                    char_right,
                    bottom,
                )
            )
            char_left = char_right
        return bounding_boxes

    def draw_on_image(
        self, image_drawer, color, image_width, image_height, fill=False, width=1
    ):
        """Draw the bounding box on an image."""
        left = self.left * image_width
        right = self.right * image_width
        top = image_height - self.top * image_height
        bottom = image_height - self.bottom * image_height
        if fill:
            image_drawer.rectangle([left, top, right, bottom], fill=color)

        else:
            image_drawer.rectangle(
                [left, top, right, bottom], outline=color, width=width
            )

    def float_to_str(self, number: float, decimal_precision: int) -> str:
        """Convert a float to a string."""
        return f"{number:.{decimal_precision}f}"

    def to_dict(self, decimal_precision: int) -> dict:
        """Convert the bounding box to a dictionary."""
        bbox_dict = {
            "left": self.float_to_str(self.left, decimal_precision),
            "top": self.float_to_str(self.top, decimal_precision),
            "right": self.float_to_str(self.right, decimal_precision),
            "bottom": self.float_to_str(self.bottom, decimal_precision),
        }
        return bbox_dict

    @classmethod
    def str_to_float(cls, number: str) -> float:
        """Convert a string to a float."""
        return float(number)

    @classmethod
    def from_dict(cls, bbox_dict: dict, decimal_precision: int) -> "BoundingBox":
        """Convert the bounding box to a dictionary."""
        left = cls.str_to_float(bbox_dict["left"])
        top = cls.str_to_float(bbox_dict["top"])
        right = cls.str_to_float(bbox_dict["right"])
        bottom = cls.str_to_float(bbox_dict["bottom"])

        try:
            return BoundingBox(left, top, right, bottom)
        except ValueError:
            epsilon = pow(10, -decimal_precision)
            if left >= right:
                right = left + epsilon
            if bottom >= top:
                top = bottom + epsilon
            return BoundingBox(left, top, right, bottom)
