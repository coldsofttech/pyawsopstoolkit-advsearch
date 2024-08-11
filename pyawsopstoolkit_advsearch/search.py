# This module supports various conditions for advanced searches, outlined below as global constants.
import re
from datetime import datetime
from typing import Any

OR: str = 'OR'  # Represents the "or" condition
AND: str = 'AND'  # Represents the "and" condition

LESS_THAN: str = 'lt'  # Represents the less than ("<") value
LESS_THAN_OR_EQUAL_TO: str = 'lte'  # Represents the less than or equal to ("<=") value
GREATER_THAN: str = 'gt'  # Represents the greater than (">") value
GREATER_THAN_OR_EQUAL_TO: str = 'gte'  # Represents the greater than or equal to (">=") value
EQUAL_TO: str = 'eq'  # Represents the equal to ("=") value
NOT_EQUAL_TO: str = 'ne'  # Represents the not equal to ("!=") value
BETWEEN: str = 'between'  # Represents the between range ("< x <") value


def _match_condition(value: str, search_field: str | list, condition: str, matched: bool) -> bool:
    """
    Matches the condition based on the specified parameters.

    :param value: The value to be evaluated.
    :type value: str
    :param search_field: The value or list of values to compare against.
    :type search_field: str | list
    :param condition: The condition to be applied: 'OR' or 'AND'.
    :type condition: str
    :param matched: The current matching status.
    :type matched: bool
    :return: Returns a boolean value (True or False) based on the comparison.
    :rtype: bool
    """
    if not value or not search_field:
        return False

    if isinstance(search_field, str):
        search_field = [search_field]

    found_match = any(re.search(value, field, re.IGNORECASE) for field in search_field)

    if condition == OR:
        return matched or found_match
    elif condition == AND:
        return matched and found_match if matched else found_match

    return matched


def _match_number_condition(value: int, search_field: int | list, condition: str, matched: bool) -> bool:
    """
    Matches the number condition based on the specified parameters.

    :param value: The value to be evaluated.
    :type value: int
    :param search_field: The value or list of values to compare against.
    :type search_field: int | list
    :param condition: The condition to be applied: 'OR' or 'AND'.
    :type condition: str
    :param matched: The current matching status.
    :type matched: bool
    :return: Returns a boolean value (True or False) based on the comparison.
    :rtype: bool
    """
    if not value or not search_field:
        return False

    if isinstance(search_field, int):
        search_field = [search_field]

    found_match = any(value == field for field in search_field)

    if condition == OR:
        return matched or found_match
    elif condition == AND:
        return matched and found_match if matched else found_match

    return matched


def _match_number_range_condition(value: int, search_field, condition: str, matched: bool) -> bool:
    """
    Matches the number range condition based on the specified parameters.

    :param value: The value to be evaluated.
    :type value: int
    :param search_field: The list of values to compare against. Format: (Value1, Value2).
    :type search_field: Any
    :param condition: The condition to be applied: 'OR' or 'AND'.
    :type condition: str
    :param matched: The current matching status.
    :type matched: bool
    :return: Returns a boolean value (True or False) based on the comparison.
    :rtype: bool
    """
    if not value or not search_field:
        return False

    found_match = False
    for _from, _to in search_field:
        if _from == -1 or _to == -1:
            found_match = True  # Case: -1 means all ports are allowed
            break
        if _from <= value <= _to:
            found_match = True
            break

    if condition == OR:
        return matched or found_match
    elif condition == AND:
        return matched and found_match if matched else found_match

    return matched


def _match_compare_condition(value: dict, search_field: Any, condition: str, matched: bool) -> bool:
    """
    Matches the condition by comparing based on the specified parameters.

    :param value: The value to be evaluated.
    :type value: dict
    :param search_field: The value to compare against.
    :type search_field: Any
    :param condition: The condition to be applied: 'OR' or 'AND'.
    :type condition: str
    :param matched: The current matching status.
    :type matched: bool
    :return: Returns a boolean value (True or False) based on the comparison.
    :rtype: bool
    """
    match = True
    if isinstance(value, dict):
        for operator, compare_value in value.items():
            if isinstance(search_field, datetime) and isinstance(compare_value, str):
                compare_value = datetime.fromisoformat(compare_value).replace(tzinfo=None)

            if operator == LESS_THAN and not search_field < compare_value:
                match = False
            elif operator == LESS_THAN_OR_EQUAL_TO and not search_field <= compare_value:
                match = False
            elif operator == EQUAL_TO and not search_field == compare_value:
                match = False
            elif operator == NOT_EQUAL_TO and not search_field != compare_value:
                match = False
            elif operator == GREATER_THAN and not search_field > compare_value:
                match = False
            elif operator == GREATER_THAN_OR_EQUAL_TO and not search_field >= compare_value:
                match = False
            elif operator == BETWEEN:
                if not isinstance(compare_value, list) or len(compare_value) != 2:
                    raise ValueError('The "between" operator requires a list of two values.')
                if isinstance(search_field, datetime):
                    compare_value[0] = datetime.fromisoformat(compare_value[0]).replace(tzinfo=None)
                    compare_value[1] = datetime.fromisoformat(compare_value[1]).replace(tzinfo=None)
                if not (compare_value[0] <= search_field <= compare_value[1]):
                    match = False
    else:
        raise ValueError('Conditions should be specified as a dictionary with operators.')

    if condition == OR and match:
        return True
    elif condition == AND and not match:
        return False

    return matched


def _match_tag_condition(value, tags, condition: str, matched: bool, key_only: bool) -> bool:
    """
    Matches the condition based on the specified tags.

    :param value: The value to be evaluated.
    :type value: Any
    :param tags: The value to compare against.
    :type tags: Any
    :param condition: The condition to be applied: 'OR' or 'AND'.
    :type condition: str
    :param matched: The current matching status.
    :type matched: bool
    :param key_only: Flag to indicate to match just key or both key and value.
    :type key_only: bool
    :return: Returns a boolean value (True or False) based on the comparison.
    :rtype: bool
    """
    match = False
    if tags is not None and len(tags) > 0:
        if key_only:
            if value in tags:
                match = True
        else:
            if tags.get(value.get('key')) == value.get('value'):
                match = True

    if condition == OR and match:
        return True
    elif condition == AND and not match:
        return False

    return matched
