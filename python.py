try:
    import expand_to_indent
    import javascript
    import utils
except:
    from . import expand_to_indent
    from . import javascript
    from . import utils


def expand(string, start, end):
    expand_stack = []
    result = javascript.expand(string, start, end)
    if result:
        return result

    expand_stack.append("line_no_indent")
    result = expand_line_without_indent(string, start, end)
    if result:
        result["expand_stack"] = expand_stack
        return result

    expand_stack.append("line_continuation")
    result = expand_over_line_continuation(string, start, end)
    if result:
        return result

    expand_stack.append("py_block_start")
    result = expand_python_block_from_start(string, start, end)
    if result:
        result["expand_stack"] = expand_stack
        return result

    expand_stack.append("py_indent")
    result = expand_to_indent.py_expand_to_indent(string, start, end)
    if result:
        result["expand_stack"] = expand_stack
        return result


def expand_over_line_continuation(string, start, end):
    if not string[end-1:end] == "\\":
        return None
    line = utils.get_line(string, start, start)
    next_line = utils.get_line(string, end + 1, end + 1)
    start = line["start"]
    end = next_line["end"]
    next_result = expand_over_line_continuation(string, start, end)
    # recursive check if there is an other continuation
    if next_result:
        start = next_result["start"]
        end = next_result["end"]
    return utils.create_return_obj(start, end, string, "line_continuation")


def expand_python_block_from_start(string, start, end):
    if string[end-1:end] != ":":
        return None
    result = expand_to_indent.expand_to_indent(string, end + 1,
                                               end + 1)
    if result:
        # line = utils.get_line(string, start, start)
        line = utils.get_line(string, start, start)
        start = line["start"]
        end = result["end"]
        return utils.create_return_obj(start, end, string, "py_block_start")


def expand_line_without_indent(string, start, end):
    line = utils.get_line(string, start, end)
    indent = expand_to_indent.get_indent(string, line)
    lstart = min(start, line["start"] + indent)
    lend = max(end, line["end"])
    if lstart != start or lend != end:
        return utils.create_return_obj(lstart, lend, string, "line_no_indent")
