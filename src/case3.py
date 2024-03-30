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

from titlecase import titlecase


def to_upper(text):
    return text.upper()


def to_lower(text):
    return text.lower()


def to_capitalized(text):
    text = string.capwords(text)
    return text


def to_sentence_case(text):
    text = text[0].upper() + text[1:].lower()
    return text


def _decorate_delimited_list(
    text, input_delimiter, trim_elements, prepend, append, output_delimiter
):
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
quote_list.__name__ = "quote_list"

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
line_break_list.__name__ = "line_break_list"

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
add_line_breaks_to_list.__name__ = "add_line_breaks_to_list"


# titlecase defined in separate file - from https://muffinresearch.co.uk/titlecasepy-titlecase-in-python/


def create_alfred_items_list(the_string):
    result = {"items": []}
    transformations = {
        "Upper Case": to_upper,
        "Lower Case": to_lower,
        "Capitalized": to_capitalized,
        "Sentence Case": to_sentence_case,
        "Title Case": titlecase,
        "Single Quote List": quote_list,
        "Line Break List": line_break_list,
        "Add Line Breaks to List": add_line_breaks_to_list,
    }

    for subtitle, func in transformations.items():
        result_string = func(the_string)
        result["items"].append(
            {
                "title": result_string,
                "subtitle": subtitle,
                "valid": True,
                "uid": func.__name__,
                "icon": {"path": "icon.png"},
                "arg": result_string,
            }
        )

    return result


def main():
    if len(sys.argv) > 1:
        the_string = sys.argv[1]
        if len(sys.argv) > 2:
            my_source = sys.argv[2]
            my_replacement_string = globals()[my_source](the_string)
            sys.stdout.write(my_replacement_string)
        else:
            result = create_alfred_items_list(the_string)
            sys.stdout.write(json.dumps(result))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
