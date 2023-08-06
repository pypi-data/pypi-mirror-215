from copy import deepcopy
from dataclasses import fields, is_dataclass
import re
from typing import Any, Dict

## Taken from: https://gist.github.com/jaytaylor/3660565#gistcomment-3228409
LEADING_UC_CAMEL_SEGMENT = re.compile(r"([A-Z]+)([A-Z][a-z])")
UC_CAMEL_SEGMENT = re.compile(r"([a-z\d])([A-Z])")


def camel_to_snake(value: str) -> str:
    """
    Convert a CamelCasedString to a snake_cased_string. Separates capitalized words with
    underscores, and lower-cases the result. Runs of multiple uppercase letters are not split, e.g.
    "HTTPPort" would become "http_port".

    :param value: a string value
    :return: the converted value
    """
    lower = value.lower()
    if value.upper() == lower:  # value is all caps
        return lower

    return UC_CAMEL_SEGMENT.sub(r"\1_\2", LEADING_UC_CAMEL_SEGMENT.sub(r"\1_\2", value)).lower()


def snake_to_camel(value: str) -> str:
    words = value.split("_")
    return words[0] + "".join([item.capitalize() for item in words[1:]])


def remove_nones_recursively(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove all None values from a dictionary recursively.
    """
    data_copy = deepcopy(data)
    for k, v in data.items():
        if v is None or v == {} or v == []:
            del data_copy[k]
        elif isinstance(v, dict):
            data_copy[k] = remove_nones_recursively(v)
        elif isinstance(v, list):
            new_items = []
            if len(v) == 1 and v[0] == {}:
                del data_copy[k]
            for item in v:
                if isinstance(item, dict):
                    new_items.append(remove_nones_recursively(item))
                else:
                    new_items.append(item)
            
            data_copy[k] = new_items

    return data_copy


def deepdiff(new_item, old_item):
    """
    Compares two dataclasses recursively and returns an object with the differences.
    
    """
    if is_dataclass(new_item) and is_dataclass(old_item):
        items = {}
        for item in fields(new_item):
            diff_items = deepdiff(getattr(new_item, item.name), getattr(old_item, item.name))
            if diff_items:
                items[item.name] = diff_items

    elif isinstance(new_item, dict):
        items = {}
        for key, value in new_item.items():
            diff_items = deepdiff(value, old_item.get(key))
            if diff_items:
                items[key] = diff_items

    elif isinstance(new_item, list):
        items = []
        if old_item is None:
            items = new_item
        else:
            for index, value in enumerate(new_item):    
                if index < len(old_item):
                    diff_items = deepdiff(value, old_item[index])
                    if diff_items:
                        items.append(diff_items)
                else:  # new item
                    items.append(value)
    elif new_item != old_item:
        return new_item
    else:
        return None

    if items == {} or items == []:
        return None

    return items