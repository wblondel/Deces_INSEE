def find_ranges(iterable):
    """Yield range of consecutive numbers."""

    from more_itertools import consecutive_groups

    for group in consecutive_groups(iterable):
        group = list(group)
        if len(group) == 1:
            yield group[0]
        else:
            yield group[0], group[-1]
