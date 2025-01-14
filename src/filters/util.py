def filter_text(removal_ranges: [tuple[int, int]], text: str) -> str:
    """
    Removes given ranges from text and returns a filtered string
    :param removal_ranges: a list of spans to remove from text
    :param text: the text to be filtered
    :return: the filtered text
    """
    offset = 0
    for span in removal_ranges:
        span = (span[0] - offset, span[1] - offset)
        text = text[:span[0]] + text[span[1]:]
        offset += (span[1] - span[0])

    return text
