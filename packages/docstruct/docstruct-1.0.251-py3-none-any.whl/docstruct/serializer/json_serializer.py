"""
Serialize and deserialize a document to and from a JSON file.
"""
from datetime import datetime
import json
from typing import Optional
from ..text_block import TextBlock, Document, Character, Word, TableType
from ..version import VERSION
from ..bounding_box import BoundingBox
from .constants import (
    BOUNDING_BOX,
    CHILDREN,
    CREATED_AT,
    DATE_FORMAT,
    DOCSTRUCT_VERSION,
    TYPE,
    MAP_TYPE_NAME_TO_CLASS,
    ID,
    TEXT_BLOCKS,
    CHILDREN_ID,
    DECIMAL_PRECISION,
    TABLE_TYPE,
)
from ..utils import type_to_params


class JsonSerializer:
    """
    A class to serialize and deserialize a document to and from a JSON file.
    """

    def serialize_document(self, document: Document) -> dict:
        """
        Serialize a document to a dict.
        """
        serialized_document = {}

        # Serialize the document
        text_blocks: list[TextBlock] = list(TextBlock.post_order_traversal(document))
        for i, text_block in enumerate(text_blocks):
            text_block.id = i
        text_block_dicts = []
        for text_block in text_blocks:
            if isinstance(text_block, Character):
                continue
            if isinstance(text_block, Word):
                children_ids = []
            else:
                children = getattr(text_block, CHILDREN, [])
                children_ids = [child.id for child in children]
            bounding_box: BoundingBox = getattr(text_block, BOUNDING_BOX, None)
            if bounding_box is not None:
                bounding_box = bounding_box.to_dict(DECIMAL_PRECISION)
            text_block_dict = {
                ID: text_block.id,
                TYPE: text_block.__class__.__name__.lower(),
                CHILDREN_ID: children_ids,
                BOUNDING_BOX: bounding_box,
            }
            params = type_to_params(text_block.__class__)
            for param in params:
                if param in [CHILDREN, BOUNDING_BOX]:
                    continue

                value = getattr(text_block, param)
                if param == TABLE_TYPE:
                    value = value.value
                text_block_dict[param] = value
            text_block_dicts.append(text_block_dict)
        serialized_document[TEXT_BLOCKS] = text_block_dicts

        # Add metadata
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime(DATE_FORMAT)
        serialized_document[CREATED_AT] = formatted_datetime
        serialized_document[DOCSTRUCT_VERSION] = VERSION

        return serialized_document

    def dump(self, document: Document, path: str):
        """
        Serialize a document to a JSON file.
        """
        json_dict = self.serialize_document(document)
        json_string = json.dumps(
            json_dict,
        )
        with open(path, "w", encoding="utf-8") as file:
            file.write(json_string)

    def load(self, path: str) -> Document:
        """
        Load a JSON file to a dict.
        """
        with open(path, "r", encoding="utf-8") as file:
            json_string = file.read()
        json_dict = json.loads(json_string)
        document = self.deserialize_document(json_dict)
        return document

    def _get_bounding_box(self, text_block_dict: dict) -> Optional[BoundingBox]:
        bounding_box_dict = text_block_dict[BOUNDING_BOX]
        if bounding_box_dict is None:
            return None
        return BoundingBox.from_dict(bounding_box_dict, DECIMAL_PRECISION)

    def _deserialize_text_block(
        self, text_block_dict: dict, map_id_to_text_block: dict
    ) -> TextBlock:
        _class = MAP_TYPE_NAME_TO_CLASS[text_block_dict[TYPE]]
        children_ids = text_block_dict.get(CHILDREN_ID, [])
        children = [map_id_to_text_block[child_id] for child_id in children_ids]
        bounding_box = self._get_bounding_box(text_block_dict)
        param_names = type_to_params(_class)
        kwargs = {
            key: value for key, value in text_block_dict.items() if key in param_names
        }
        if CHILDREN in param_names:
            kwargs[CHILDREN] = children
        if BOUNDING_BOX in param_names:
            kwargs[BOUNDING_BOX] = bounding_box
        if TABLE_TYPE in param_names:
            kwargs[TABLE_TYPE] = TableType(kwargs[TABLE_TYPE])
        text_block = _class(**kwargs)
        return text_block

    def deserialize_document(self, json_dict: dict) -> Document:
        """
        Deserialize a dict to a document.
        """
        text_block_dicts: list[dict] = json_dict[TEXT_BLOCKS]
        map_id_to_text_block = {}
        max_id = 0
        for text_block_dict in text_block_dicts:  # post-order traversal
            text_block_id = text_block_dict[ID]
            text_block = self._deserialize_text_block(
                text_block_dict, map_id_to_text_block
            )
            map_id_to_text_block[text_block_id] = text_block
            max_id = max(max_id, text_block_id)
        document = map_id_to_text_block[max_id]
        return document
