import re

try:
    import expand_to_regex_set
except:
    from . import expand_to_regex_set


def expand_to_subword(string, start, end):
    # if it is an upper case word search for upper case chars
    # else search for lower case chars
    if(_is_inside_upper(string, start, end)):
        regex = re.compile(r"[A-Z]")
    else:
        regex = re.compile(r"[a-z]")

    result = expand_to_regex_set._expand_to_regex_rule(
        string, start, end, regex, "subword")
    if result is None:
        return None
    # check if it is prefixed by an upper char
    # expand from camelC|ase| to camel|Case|
    upper = re.compile(r"[A-Z]")
    if upper.match(string[result["start"]-1:result["start"]]):
        result["start"] -= 1
    # check that it is a "true" subword, i.e. inside a word
    if not _is_true_subword(string, result):
        return None
    return result


def _is_true_subword(string, result):
    start = result["start"]
    end = result["end"]
    char_before = string[start-1:start]
    char_after = string[end:end+1]
    is_word_before = re.match(r"[a-z0-9_]", char_before, re.IGNORECASE)
    is_word_after = re.match(r"[a-z0-9_]", char_after, re.IGNORECASE)
    return bool(is_word_before or is_word_after)


def _is_inside_upper(string, start, end):
    if start != end:
        return string[start:end].isupper()
    start = max(0, start-2)
    end = min(end + 2, len(string))
    sub_str = string[start:end]
    contains_upper = re.search(r"[A-Z]{2}", sub_str)
    sub_str = sub_str[1:3]
    contains_lower = re.search(r"[a-z]", sub_str)
    return bool(contains_upper) and not bool(contains_lower)
