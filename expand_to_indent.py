import re

try:
    # Block it from trying to import something which should not be on the python sys.path
    # https://github.com/hktonylee/SublimeNumberKing/issues/4
    import expand_region_handler
    import utils
except:
    from . import utils


_INDENT_RE = re.compile(r"^(?P<spaces>\s*)")


def empty_line(string, line):
    return not string[line["start"]:line["end"]].strip()


def get_indent(string, line):
    line_str = string[line["start"]:line["end"]]
    m = _INDENT_RE.match(line_str)
    if m is None:  # should never happen
        return 0
    return len(m.group("spaces"))


def _expand_to_indent(string, start, end):
    line = utils.get_line(string, start, end)
    indent = get_indent(string, line)
    start = line["start"]
    end = line["end"]
    before_line = line
    while True:
        # get the line before
        pos = before_line["start"] - 1
        if pos <= 0:
            break
        before_line = utils.get_line(string, pos, pos)
        before_indent = get_indent(string, before_line)
        # done if the line has a lower indent
        if not indent <= before_indent and not empty_line(string, before_line):
            break
        # if the indent equals the lines indent than update the start
        if not empty_line(string, before_line) and indent == before_indent:
            start = before_line["start"]

    after_line = line
    while True:
        # get the line after
        pos = after_line["end"] + 1
        if pos >= len(string):
            break
        after_line = utils.get_line(string, pos, pos)
        after_indent = get_indent(string, after_line)
        # done if the line has a lower indent
        if not indent <= after_indent and not empty_line(string, after_line):
            break
        # move the end
        if not empty_line(string, after_line):
            end = after_line["end"]

    return utils.create_return_obj(start, end, string, "indent")


def expand_to_indent(string, start, end):
    result = _expand_to_indent(string, start, end)
    if result["start"] == start and result["end"] == end:
        return None
    return result


def py_expand_to_indent(string, start,
                        end):
    line = utils.get_line(string, start, end)
    indent = get_indent(string, line)
    # we don't expand to indent 0 (whole document)
    if indent == 0:
        return None
    # expand to indent
    result = _expand_to_indent(string, start, end)
    if result is None:
        return None
    # get the intent of the first lin
    # if the expansion changed return the result increased
    if not(result["start"] == start and result["end"] == end):
        return result
    pos = result["start"] - 1
    while True:
        if pos < 0:
            return None
        # get the indent of the line before
        before_line = utils.get_line(string, pos, pos)
        before_indent = get_indent(string, before_line)
        if not empty_line(string, before_line) and before_indent < indent:
            start = before_line["start"]
            end = result["end"]
            return utils.create_return_obj(start, end, string, "py_indent")
        # goto the line before the line befor
        pos = before_line["start"] - 1
