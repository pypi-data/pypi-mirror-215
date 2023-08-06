"""
Constants used in the serializer module.
"""
from ..text_block import (
    Word,
    Document,
    Page,
    Line,
    Paragraph,
    Table,
    TableColumn,
    TableCell,
)

DOCUMENT = "document"
PAGE = "page"
LINE = "line"
PARAGRAPH = "paragraph"
WORD = "word"
TABLE = "table"
TABLE_COLUMN = "tablecolumn"
TABLE_CELL = "tablecell"
BOUNDING_BOX = "bounding_box"


MAP_TYPE_NAME_TO_CLASS = {
    DOCUMENT: Document,
    PAGE: Page,
    LINE: Line,
    PARAGRAPH: Paragraph,
    WORD: Word,
    TABLE: Table,
    TABLE_COLUMN: TableColumn,
    TABLE_CELL: TableCell,
}

SELF = "self"
ID = "id"
TEXT_BLOCKS = "text_blocks"
TYPE = "type"
PARAMS = "params"
CHILDREN = "children"
CREATED_AT = "created_at"
DATE_FORMAT = "%Y-%m-%d %H:%M"
DOCSTRUCT_VERSION = "docstruct_version"
CHILDREN_ID = "children_id"
TABLE_TYPE = "table_type"
DECIMAL_PRECISION = 3
