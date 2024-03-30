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
import os
import string
import sys
from functools import partial

from titlecase import titlecase


def SendDown(key):
    string = str(key)
    cmd = (
        """osascript -e 'tell application "System Events" to key down (key code """
        + string
        + ")'"
    )
    os.system(cmd)


def copy_selection():
    SendDown(8)


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

# titlecase defined in separate file - from https://muffinresearch.co.uk/titlecasepy-titlecase-in-python/


def produceOutput(theString):
    result = {"items": []}
    # Add items to Alfred feedback with uids so Alfred will track frequency of use

    resultString = to_upper(theString)
    result["items"].append(
        {
            "title": resultString,
            "subtitle": "Upper Case",
            "valid": True,
            "uid": "uppercase",
            "icon": {"path": "icon.png"},
            "arg": resultString,
        }
    )

    resultString = to_lower(theString)
    result["items"].append(
        {
            "title": resultString,
            "subtitle": "Lower Case",
            "valid": True,
            "uid": "lowercase",
            "icon": {"path": "icon.png"},
            "arg": resultString,
        }
    )

    resultString = to_capitalized(theString)
    result["items"].append(
        {
            "title": resultString,
            "subtitle": "Capitalized",
            "valid": True,
            "uid": "Capitalized",
            "icon": {"path": "icon.png"},
            "arg": resultString,
        }
    )

    resultString = to_sentence_case(theString)
    result["items"].append(
        {
            "title": resultString,
            "subtitle": "Sentence Case",
            "valid": True,
            "uid": "Sentencecase",
            "icon": {"path": "icon.png"},
            "arg": resultString,
        }
    )

    resultString = titlecase(theString)
    result["items"].append(
        {
            "title": resultString,
            "subtitle": "Title Case",
            "valid": True,
            "uid": "titlecase",
            "icon": {"path": "icon.png"},
            "arg": resultString,
        }
    )

    resultString = quote_list(theString)
    result["items"].append(
        {
            "title": resultString,
            "subtitle": "Single Quote List",
            "valid": True,
            "uid": "Quotelist",
            "icon": {"path": "icon.png"},
            "arg": resultString,
        }
    )

    resultString = line_break_list(theString)
    result["items"].append(
        {
            "title": resultString,
            "subtitle": "Line Break List",
            "valid": True,
            "uid": "Linebreaklist",
            "icon": {"path": "icon.png"},
            "arg": resultString,
        }
    )

    resultString = add_line_breaks_to_list(theString)
    result["items"].append(
        {
            "title": resultString,
            "subtitle": "Add Line Breaks to List",
            "valid": True,
            "uid": "Addlinebreakstolist",
            "icon": {"path": "icon.png"},
            "arg": resultString,
        }
    )

    print(json.dumps(result))


def main():
    if len(sys.argv) > 2:
        theString = sys.argv[1]
        mySource = sys.argv[2]

        myReplacementString = eval(mySource)

        myReplacementString = globals()[mySource](theString)
        sys.stdout.write(myReplacementString)
        sys.stdout.flush()

    else:
        theString = sys.argv[1]
        produceOutput(theString)


if __name__ == "__main__":
    main()
