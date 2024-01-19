from typing import List
import sqlalchemy


def remove_private_attributes(obj) -> dict:
    return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}


# Extract ids from format: "-1-2-3-"
def extract_ids(ids_str: str) -> List[int]:
    return [int(id) for id in ids_str.split("-") if id]


# Format list of ids to string: "-1-2-3-"
def format_str_ids(ids: List[int]):
    return "-" + "-".join([str(id) for id in ids]) + "-"


def object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key) for c in sqlalchemy.inspect(obj).mapper.column_attrs
    }
