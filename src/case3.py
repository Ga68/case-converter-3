#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# case3.py
#
# 2022-03-26 converted to Python 3
# removed dependency on deanishe's Alfred Workflow library

# 2014-09-10 by Derick Fay
#
# original inspiration from jdc0589's CaseConversion plug-in for SublimeText:
# https://github.com/jdc0589/CaseConversion/blob/master/case_conversion.py
#
#

import json
import string
import sys
from functools import partial
from typing import Any, Callable, Dict, List

# from https://muffinresearch.co.uk/titlecasepy-titlecase-in-python/
from titlecase import titlecase


def to_upper(text: str) -> str:
    return text.upper()


def to_lower(text: str) -> str:
    return text.lower()


def to_capitalized(text: str) -> str:
    text = string.capwords(text)
    return text


def to_sentence_case(text: str) -> str:
    text = text[0].upper() + text[1:].lower()
    return text


def _decorate_delimited_list(
    text: str,
    input_delimiter: str,
    trim_elements: bool,
    prepend: str,
    append: str,
    output_delimiter: str,
) -> str:
    """a generic function to read in, amend, and output a list"""
    text_list = text.split(input_delimiter)
    if trim_elements:
        text_list = [elem.strip() for elem in text_list if elem.strip()]
    return output_delimiter.join([f"{prepend}{elem}{append}" for elem in text_list])


# add single quotes to a list, with clean up, such that "1, 2,3,,4" becomes
# '1', '2', '3', '4'
quote_list = partial(
    _decorate_delimited_list,
    input_delimiter=",",
    trim_elements=True,
    prepend="'",
    append="'",
    output_delimiter=", ",
)

# convert a list into lines, with clean up, such that "1, 2,3,,4" becomes
# 1
# 2
# 3
# 4
line_break_list = partial(
    _decorate_delimited_list,
    input_delimiter=",",
    trim_elements=True,
    prepend="",
    append="",
    output_delimiter="\n",
)

# convert a list into a list of lines, with clean up, such that "1, 2,3,,4" becomes
# 1,
# 2,
# 3,
# 4
add_line_breaks_to_list = partial(
    _decorate_delimited_list,
    input_delimiter=",",
    trim_elements=True,
    prepend="",
    append="",
    output_delimiter=",\n",
)


def create_alfred_items_object(text: str) -> Dict[str, List[Dict[str, Any]]]:
    result: Dict[str, List[Dict[str, Any]]] = {"items": []}
    # the dictionary of function display names mapping to the functions themselves
    transformations: Dict[str, Callable[[str], str]] = {
        "Upper Case": to_upper,
        "Lower Case": to_lower,
        "Capitalized": to_capitalized,
        "Sentence Case": to_sentence_case,
        "Single Quote List": quote_list,
        "Line Break List": line_break_list,
        "Add Line Breaks to List": add_line_breaks_to_list,
        # titlecase defined in separate file and imported at top
        "Title Case": titlecase,
    }

    for display_name, func in transformations.items():
        transformed_text = func(text)
        result["items"].append(
            {
                "title": transformed_text,
                "subtitle": display_name,
                "valid": True,
                "uid": display_name.lower().replace(" ", "_"),
                "icon": {"path": "icon.png"},
                "arg": transformed_text,
            }
        )

    return result


def main() -> None:
    if len(sys.argv) < 2:
        raise ValueError("at least one command line argument needed")

    the_string = sys.argv[1]
    if len(sys.argv) == 2:  # one command line argument
        output = json.dumps(create_alfred_items_object(the_string))
    elif len(sys.argv) == 3:  # two command line arguments
        func = globals()[sys.argv[2]]
        output = func(the_string)
    else:
        raise ValueError("no more than two command line arguments are expected")

    sys.stdout.write(output)
    sys.stdout.flush()


if __name__ == "__main__":
    main()
