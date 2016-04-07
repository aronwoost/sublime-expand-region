import re
try:
    import expand_to_regex_set
    import expand_to_symbols
    import utils
    _ST3 = False
except:
    from . import expand_to_regex_set
    from . import expand_to_symbols
    from . import utils
    _ST3 = True


_BEGIN_END_REG = re.compile(
    r"\\(?P<command>begin|end)"
    r"(?:\[.*\])?"
    r"\{(?P<name>[^\}]*)\}"
)
_EXCLUSIVE_BEGIN_END_REG = re.compile(
    r"^"
    r"\\(?P<command>begin|end)"
    r"(?:\[.*\])?"
    r"\{(?P<name>[^\}]*)\}"
    r"$"
)


def chart_at(string, index):
    """returns the chart at the position or the empty string,
    if the index is outside the string"""
    return string[index:index+1]


def expand_to_tex_word(string, start, end):
    """Expand to a valid latex word."""
    regex = re.compile(r"[a-zA-Z@]", re.UNICODE)

    return expand_to_regex_set._expand_to_regex_rule(
        string, start, end, regex, "tex_word")


def _get_closest_env_border(string, start_pos, end_pos, reverse=False):
    open_command = "begin"
    close_command = "end"
    if _ST3:
        iterator = _BEGIN_END_REG.finditer(string, pos=start_pos,
                                           endpos=end_pos)
        offset = 0
    else:
        s = string[start_pos:end_pos]
        iterator = _BEGIN_END_REG.finditer(s)
        offset = start_pos
    if reverse:
        iterator = reversed(list(iterator))
        open_command, close_command = close_command, open_command
    count = 0
    for before in iterator:
        line = utils.get_line(string, before.start(), before.end())
        # ignore comment lines
        if string[line["start"]:line["end"]].strip()[0] == "%":
            continue
        command = before.group("command")
        if command == open_command:
            count += 1
        elif command == close_command and count > 0:
            count -= 1
        elif command == close_command:
            # found begin before
            return {
                "start": offset + before.start(),
                "end": offset + before.end(),
                "name": before.group("name")
            }


def expand_against_matching_env(string, start, end):
    m = _EXCLUSIVE_BEGIN_END_REG.match(string[start:end])
    if not m:
        return None
    if m.group("command") == "begin":
        reverse = False  # search downwards
        search_start = end
        search_end = len(string)
    else:  # == "end"
        reverse = True  # search upwards
        search_start = 0
        search_end = start
    env_border = _get_closest_env_border(string, search_start, search_end,
                                         reverse=reverse)
    if not env_border:
        return None
    if not env_border["name"] == m.group("name"):
        print("Environments not matching '{}' and '{}'"
              .format(env_border["name"], m.group("name")))
        return None
    if not reverse:  # search from begin
        start = start
        end = env_border["end"]
    else:  # search from end
        start = env_border["start"]
        end = end
    return utils.create_return_obj(start, end, string,
                                   "latex_environment_matching")


def expand_against_env(string, start, end):
    tex_begin = _get_closest_env_border(string, 0, start, reverse=True)
    tex_end = _get_closest_env_border(string, end, len(string), reverse=False)

    if tex_begin is None or tex_end is None:
        return None
    if tex_begin["name"] != tex_end["name"]:
        print("Environments not matching '{}' and '{}'"
              .format(tex_begin["name"], tex_end["name"]))
        return None
    inner_env_selected = start == tex_begin["end"] and end == tex_end["start"]
    if inner_env_selected:
        start = tex_begin["start"]
        end = tex_end["end"]
    else:
        start = tex_begin["end"]
        end = tex_end["start"]
    return utils.create_return_obj(start, end, string, "latex_environment")


def expand_agains_base_command(string, start, end):
    start -= 1
    if chart_at(string, start) == "\\":
        if chart_at(string, end) == "*":
            end += 1
        result = utils.create_return_obj(start, end, string,
                                         "latex_command_base")
        return result


class NoSemanticUnit(Exception):
    pass


def _stretch_over_previous_semantic_unit(string, start):
    start -= 1
    while chart_at(string, start) == " ":
        start -= 1
    if chart_at(string, start) in ["]", "}"]:
        r = expand_to_symbols.expand_to_symbols(string, start, start)
        if r is not None:
            return r["start"] - 1
    raise NoSemanticUnit()


def _stretch_over_next_semantic_unit(string, end):
    while chart_at(string, end) == " ":
        end += 1
    if chart_at(string, end) in ["[", "{"]:
        end += 1
        r = expand_to_symbols.expand_to_symbols(string, end, end)
        if r is not None:
            end = r["end"]
            # special case: '{}' (no content)
            if end == r["start"] + 2:
                return end
            return end + 1
    raise NoSemanticUnit()


def expand_against_command_args(string, start, end):
    if not chart_at(string, start) == "\\":
        return None
    if chart_at(string, end) not in ["{", "["]:
        return None
    original_end = end
    while True:
        try:
            end = _stretch_over_next_semantic_unit(string, end)
        except NoSemanticUnit:
            break
    # if the end did not change: do nothing
    if original_end == end:
        return None
    return utils.create_return_obj(start, end, string, "latex_command_arg")


def expand_against_surrounding_command(string, start, end):
    if chart_at(string, start) in ["{", "["] and\
            chart_at(string, end - 1) in ["}", "]"]:
        # span backwards over [..] and {..}
        while True:
            try:
                start = _stretch_over_previous_semantic_unit(string, start)
            except NoSemanticUnit:
                break
        # span forwards over [..]  and [..]
        while True:
            try:
                end = _stretch_over_next_semantic_unit(string, end)
            except NoSemanticUnit:
                break

        # span over the previous \command or \command*
        if chart_at(string, start - 1) == "*":
            start -= 1
        result = expand_to_tex_word(string, start, start)
        if result is None:
            return None
        start = result["start"] - 1
        if chart_at(string, start) == "\\":
            return utils.create_return_obj(start, end, string,
                                           "latex_command_surround")


def expand_to_inline_math(string, start, end):
    # don't expand if a dollar sign is inside the string
    if re.search(r"(?:[^\\]|^)\$", string[start:end]):
        return

    line = utils.get_line(string, start, end)
    escape = inside = False
    open_pos = close_pos = None
    # we only need to consider one position, because we have checked it does
    # not contain any $-signs
    pos = start - line["start"]
    for i, char in enumerate(string[line["start"]:line["end"]]):
        # break if we are behind
        behind = pos < i
        if not inside and behind:
            return
        if escape:
            escape = False
        elif char == "\\":
            escape = True
            continue
        elif char == "$":
            if not inside:
                # the inner end of the $-sign
                open_pos = i + 1
            elif behind:
                close_pos = i
                break
            inside = not inside

    if open_pos is not None and close_pos is not None:
        open_pos = line["start"] + open_pos
        close_pos = line["start"] + close_pos
        # expand to the outer end
        if open_pos == start and close_pos == end:
            open_pos -= 1
            close_pos += 1
        return utils.create_return_obj(
            open_pos, close_pos, string, "latex_inline_math")


# TODO could be moved to utils?
def _closest_result(result1, result2):
    if result1 is None:
        return result2
    if result2 is None:
        return result1
    if result1["start"] < result2["start"] and\
            result2["end"] < result1["end"]:
        return result2
    else:
        return result1


def expand(string, start, end):
    expand_stack = []

    expand_stack.append("tex_word")

    result = expand_to_tex_word(string, start, end)
    if result:
        result["expand_stack"] = expand_stack
        return result

    expand_stack.append("latex_command_base")

    result = expand_agains_base_command(string, start, end)
    if result:
        result["expand_stack"] = expand_stack
        return result

    expand_stack.append("tex_math_command")

    # expand to math commands, e.g. \phi_x^2
    regex = re.compile(r"[\w\\@^]", re.UNICODE)
    result = expand_to_regex_set._expand_to_regex_rule(
        string, start, end, regex, "tex_math_command")
    if result:
        result["expand_stack"] = expand_stack
        return result

    expand_stack = ["latex_command_arg"]

    result = expand_against_command_args(string, start, end)
    if result:
        result["expand_stack"] = expand_stack
        return result

    expand_stack.append("latex_command_surround")

    result = expand_against_surrounding_command(string, start, end)
    if result:
        result["expand_stack"] = expand_stack
        return result

    expand_stack.append("latex_inline_math")

    result = expand_to_inline_math(string, start, end)
    if result:
        result["expand_stack"] = expand_stack
        return result

    expand_stack.append("latex_environment_matching")

    result = expand_against_matching_env(string, start, end)
    if result:
        result["expand_stack"] = expand_stack
        return result

    env_result = expand_against_env(string, start, end)

    # there might be a {} inside the environment
    sym_result = expand_to_symbols.expand_to_symbols(string, start, end)
    result = _closest_result(env_result, sym_result)
    if result == env_result:
        expand_stack.append("latex_environment")
    else:
        expand_stack.append("symbols")

    if result:
        result["expand_stack"] = expand_stack
        return result
