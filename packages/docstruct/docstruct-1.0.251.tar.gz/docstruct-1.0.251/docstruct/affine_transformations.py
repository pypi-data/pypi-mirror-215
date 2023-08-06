"""
This module contains the classes to handle affine transformations.
"""
import numpy as np
from .text_block import Page
from .bounding_box import BoundingBox
from .point import Point


def normalize(page: Page) -> "LinearTransformation":
    """
    Get the matrix to normalize the coordinates of page A
    The matrix is 3x3, handling the x, y, and 1 coordinates
    """
    normalize_matrix = np.array(
        [
            [1 / page.width, 0, 0],
            [0, 1 / page.height, 0],
            [0, 0, 1],
        ]
    )
    return LinearTransformation(normalize_matrix)


def denormalize(page: Page) -> "LinearTransformation":
    """
    Get the matrix to normalize the coordinates of page A
    The matrix is 3x3, handling the x, y, and 1 coordinates
    """
    normalize_matrix = np.array(
        [
            [page.width, 0, 0],
            [0, page.height, 0],
            [0, 0, 1],
        ]
    )
    return LinearTransformation(normalize_matrix)


def accuracy_test(
    transformation: "AffineTransformation",
    matched_points: list[tuple[Point, Point]],
) -> float:
    """
    Test the accuracy of the transform by calculating the average distance
    between the transformed points and the points on page B.
    The matched points should be normalized in the case the transform is normalized.
    """
    total_distance = 0
    for point_a, point_b in matched_points:
        transformed_point = transformation.transform_point(point_a)
        current_distance = transformed_point.distance(point_b)
        total_distance += current_distance
    return total_distance / len(matched_points)


class AffineTransformation:
    """
    An affine transformation is a combination of linear transformations and translations
    """

    def __init__(self, matrix: np.ndarray):
        """
        Initialize the affine transformation with a 3x3 matrix
        """
        self.matrix = matrix

    def convert_point_to_array(self, point: Point) -> np.ndarray:
        """
        Convert a point to array
        """
        return np.array([point.x, point.y, 1])

    def convert_array_to_point(self, array: np.ndarray) -> Point:
        """
        Convert an array to a point
        """
        return Point(array[0], array[1])

    def transform_bounding_box(self, bounding_box: BoundingBox) -> BoundingBox:
        """
        Transform a bounding box from page A to page B
        """
        top_left = self.transform_point(bounding_box.get_top_left())
        bottom_right = self.transform_point(bounding_box.get_bottom_right())
        return BoundingBox(
            left=top_left.x,
            top=top_left.y,
            right=bottom_right.x,
            bottom=bottom_right.y,
        )

    def transform_point(self, point: Point) -> Point:
        """
        Transform a point
        """
        array = self.convert_point_to_array(point)
        transformed_array = self.matrix @ array
        return self.convert_array_to_point(transformed_array)

    @staticmethod
    def concatenate_transformations(
        *transformations: "AffineTransformation",
    ) -> "AffineTransformation":
        """
        Concatenate multiple affine transformations
        """
        matrix = np.eye(3)
        for transformation in transformations:
            matrix = transformation.matrix @ matrix
        return AffineTransformation(matrix)

    def concatenate(
        self,
        other: "AffineTransformation",
    ) -> "AffineTransformation":
        """
        Concatenate multiple affine transformations
        """
        matrix = other.matrix @ self.matrix
        return AffineTransformation(matrix)

    def normalize_transformation(
        self, page_a: Page, page_b: Page
    ) -> "AffineTransformation":
        """
        Get the normalized transform from page A to page B
        """
        denormalize_page_a = denormalize(page_a)
        normalize_page_b = normalize(page_b)
        normalized_transformation = denormalize_page_a.concatenate(
            self
        ).concatenate(normalize_page_b)
        return normalized_transformation


class Translation(AffineTransformation):
    """
    A translation is a transformation that moves a point
    """

    def __init__(self, x_translation: float, y_translation: float):
        matrix = self._get_translation_matrix(x_translation, y_translation)
        super().__init__(matrix)

    def _get_translation_matrix(
        self, x_translation: float, y_translation: float
    ) -> np.ndarray:
        """
        Get the 3x3 translation matrix for the given dx and dy
        """
        return np.array(
            ((1, 0, x_translation), (0, 1, y_translation), (0, 0, 1))
        )


class LinearTransformation(AffineTransformation):
    """
    A linear transformation is a transformation that can be represented by a matrix multiplication
    """

    def __init__(self, matrix: np.ndarray):
        """
        Initialize the linear transformation with a 2x2 matrix
        """
        super().__init__(matrix)


class Rotation(LinearTransformation):
    """
    A rotation is a transformation that rotates a point around a center
    """

    def __init__(self, angle: float):
        self.angle = angle
        matrix = self._get_rotation_matrix(angle)
        super().__init__(matrix)

    def _get_rotation_matrix(self, angle: float) -> np.ndarray:
        """
        Get the 3x3 rotation matrix for the given angle
        """
        rad_angle = np.radians(angle)
        cos, sin = np.cos(rad_angle), np.sin(rad_angle)
        return np.array(((cos, -sin, 0), (sin, cos, 0), (0, 0, 1)))


class Scaling(LinearTransformation):
    """
    A scale is a transformation that scales a point around a center
    """

    def __init__(self, scale: float):
        self.scale = scale
        matrix = self._get_scale_matrix(scale)
        super().__init__(matrix)

    def _get_scale_matrix(self, scale) -> np.ndarray:
        """
        Get the 3x3 scale matrix for the given scale
        """
        return np.array(((scale, 0, 0), (0, scale, 0), (0, 0, 1)))
