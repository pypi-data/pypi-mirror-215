"""
The page alignment module is responsible for aligning two pages.
The current alignment is assumed to be a combination of 
translation, rotation, and scaling.
The alignment is done by 
1. matching words between the two pages.
2. using RANSAC to find the best affine transform between the two pages.
"""

from itertools import combinations
import random
from typing import Optional
import numpy as np

import attr
from sklearn.linear_model import RANSACRegressor, LinearRegression
from .text_block import Page, Word
from .point import Point
from .affine_transformations import AffineTransformation
from .constants import (
    PAGE_ALIGNMENT_MAX_MATCH,
    PAGE_ALIGNMENT_MIN_MATCH,
    RANDOM_SEED,
    PAGE_ALIGNMENT_MAX_ANGLE,
)


@attr.s(auto_attribs=True)
class MatchedWords:
    """
    A pair of words that are matched between two pages
    """

    word_a: Word
    word_b: Word


class MatchedPoints:
    """
    A pair of points that are matched between two pages
    """

    def __init__(self, point_a: Point, point_b: Point):
        self.point_a = point_a
        self.point_b = point_b
        self.good_score = 0
        self.bad_score = 0


class PageAligner:
    """
    The page aligner aligns two pages.
    """

    def __init__(
        self, page_a: Page, page_b: Page, distance_threshold: float = 0.3
    ):
        self.page_a = page_a
        self.page_b = page_b
        self.distance_threshold = distance_threshold

    def ransac_regression(
        self, x_values: list[list[float, float]], y_values: list[float]
    ) -> np.ndarray:
        """
        Fit a RANSAC regression to the data of the form z = x_coef*x + y_coef*y + b
        """
        ransac = RANSACRegressor()
        ransac.fit(x_values, y_values)
        transform = []
        x_coef = ransac.estimator_.coef_[0]
        y_coef = ransac.estimator_.coef_[1]
        intercept = ransac.estimator_.intercept_
        transform = np.array([x_coef, y_coef, intercept])
        return transform

    def get_affine_transform(
        self, matched_points: list[MatchedPoints]
    ) -> AffineTransformation:
        """
        Get the affine transform from page A to page B
        """
        a_values = [(p.point_a.x, p.point_a.y) for p in matched_points]
        b_x_values = [p.point_b.x for p in matched_points]
        b_y_values = [p.point_b.y for p in matched_points]
        x_transform = self.ransac_regression(a_values, b_x_values).reshape(
            1, 3
        )
        y_transform = self.ransac_regression(a_values, b_y_values).reshape(
            1, 3
        )
        third_row = np.array([0, 0, 1]).reshape(1, 3)
        affine_transform = np.concatenate(
            (x_transform, y_transform, third_row), axis=0
        )
        return AffineTransformation(affine_transform)

    def get_similarity_transform(
        self, matched_points: list[MatchedPoints]
    ) -> AffineTransformation:
        """
        A similarity transform is a transform that preserves the shape of the object
        but can change the size and orientation.
        It is a combination of a rotation, a scaling and translation.
        A general similarity transform is of the form:
        [[u, -v, bx], [v, u, by]].
        Given a point (x,y) we embed it in R3 as (x, y, 1).
        The result of the transform is [[u, -v], [v, u]] * (x, y) + [bx,by]
        where the first matrix is combination of rotation and scaling.
        A single matching point gives two equations:
        u*x - v*y + bx = x'
        v*x + u*y + by = y'
        We can solve for u, v, bx, by using RANSAC regression without intercept.
        """
        x_independent = [
            (p.point_a.x, -p.point_a.y, 1, 0) for p in matched_points
        ]
        y_independent = [
            (p.point_a.y, p.point_a.x, 0, 1) for p in matched_points
        ]
        x_dependent = [p.point_b.x for p in matched_points]
        y_dependent = [p.point_b.y for p in matched_points]
        independent = x_independent + y_independent
        dependent = x_dependent + y_dependent
        base_estimator = LinearRegression(fit_intercept=False)
        ransac = RANSACRegressor(base_estimator=base_estimator)
        ransac.fit(independent, dependent)
        (
            cosine_element,
            sin_element,
            intercept_x,
            intercept_y,
        ) = ransac.estimator_.coef_
        similarity_transform = np.array(
            [
                [cosine_element, -sin_element, intercept_x],
                [sin_element, cosine_element, intercept_y],
                [0, 0, 1],
            ]
        )
        return AffineTransformation(similarity_transform)

    def map_words_str_to_words(self, words: list[Word]) -> dict[str, list]:
        """
        Map the words to a dictionary where the key is the word string
        and the value is a list of words
        """
        mapped_words: dict[str, list] = {}
        for word in words:
            if word.text in mapped_words:
                mapped_words[word.text].append(word)
            else:
                mapped_words[word.text] = [word]
        return mapped_words

    def get_matched_words(
        self, a_words: list[Word], b_words: list[Word]
    ) -> list[MatchedWords]:
        """
        Get the matched words between the two pages.
        """

        a_map_words = self.map_words_str_to_words(a_words)
        b_map_words = self.map_words_str_to_words(b_words)

        matched_words: list[MatchedWords] = []

        for a_word in a_words:
            associated_a_words = a_map_words.get(a_word.text, [])
            associated_b_words = b_map_words.get(a_word.text, [])
            if len(associated_a_words) != 1 or len(associated_b_words) != 1:
                continue
            b_word = associated_b_words[0]
            matched_words.append(MatchedWords(a_word, b_word))
        return matched_words

    def denormalize_matched_points(
        self, matched_points: list[MatchedPoints]
    ) -> list[MatchedPoints]:
        """
        Denormalize the matched points to the original page coordinates
        """
        denormalized_points: list[MatchedPoints] = []
        for matched_point in matched_points:
            denormalized_points.append(
                MatchedPoints(
                    self.page_a.denormalize_point(matched_point.point_a),
                    self.page_b.denormalize_point(matched_point.point_b),
                )
            )
        return denormalized_points

    def get_matched_points(
        self, matched_words: list[MatchedWords]
    ) -> list[MatchedPoints]:
        """
        Get the matched points from the center of the matched words
        """
        matched_points: list[MatchedPoints] = []
        for matched_word in matched_words:
            a_point = matched_word.word_a.bounding_box.get_center()
            b_point = matched_word.word_b.bounding_box.get_center()
            matched_points.append(
                MatchedPoints(
                    a_point,
                    b_point,
                )
            )
        return matched_points

    def is_bad_triplet(
        self, triplet: tuple[MatchedPoints, MatchedPoints, MatchedPoints]
    ) -> bool:
        """
        Check if the triplet is a bad triplet
        """
        match_1, match_2, match_3 = triplet

        a_angle = Point.get_angle(
            match_1.point_a, match_2.point_a, match_3.point_a
        )
        b_angle = Point.get_angle(
            match_1.point_b, match_2.point_b, match_3.point_b
        )
        angle_diff = abs(a_angle - b_angle)
        if angle_diff > PAGE_ALIGNMENT_MAX_ANGLE:
            return True
        return False

    def filter_matched_points(
        self, matched_points: list[MatchedPoints]
    ) -> list[MatchedPoints]:
        """
        Filter the matched points to remove bad matches.
        We assume that there exists a similarity transform between the two pages.
        Therefore the angles between the matched points should be "equal".
        We go over all the triplets of matched points and check if the angles
        are "equal". If not, we give bad score to the matched points.
        """
        if len(matched_points) < 3:
            return matched_points
        max_number_matches = min(PAGE_ALIGNMENT_MAX_MATCH, len(matched_points))
        random.seed(RANDOM_SEED)
        matched_points = random.sample(matched_points, max_number_matches)
        matched_points_triplets = list(combinations(matched_points, 3))
        for triplet in matched_points_triplets:
            if self.is_bad_triplet(triplet):
                for match in triplet:
                    match.bad_score += 1

            else:
                for match in triplet:
                    match.good_score += 1

        filtered_matched_points = []
        for match in matched_points:
            if match.good_score > match.bad_score:
                filtered_matched_points.append(match)
        return filtered_matched_points

    def get_alignment_transform(self) -> Optional[AffineTransformation]:
        """
        Get the alignment transform between the two pages
        """
        a_words = list(self.page_a.get_all(Word))
        b_words = list(self.page_b.get_all(Word))
        matched_words: list[MatchedWords] = self.get_matched_words(
            a_words, b_words
        )
        matched_points: list[MatchedPoints] = self.get_matched_points(
            matched_words
        )
        matched_points = self.denormalize_matched_points(matched_points)
        matched_points = self.filter_matched_points(matched_points)
        if len(matched_points) < PAGE_ALIGNMENT_MIN_MATCH:
            return None

        similarity_transform = self.get_similarity_transform(matched_points)
        similarity_transform = similarity_transform.normalize_transformation(
            self.page_a, self.page_b
        )
        return similarity_transform
