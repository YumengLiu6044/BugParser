class CodeRegion:
    """A class that represents a java code region."""
    def __init__(
        self,
        region_type: str,
        span: tuple[int, int],
        source_code: str
    ):
        self._type = region_type
        self._span = span
        self._source_code = source_code

    @property
    def type(self) -> str:
        return self._type

    @property
    def span(self) -> tuple[int, int]:
        return self._span

    @property
    def source_code(self) -> str:
        return self._source_code

    def __repr__(self):
        output = f"\nRegion type: {self._type}\n"
        output += f"Span: {self._span}\n"
        output += f"Source code: {self._source_code}\n"
        return output

    def __le__(self, other):
        return self.span[0] <= other.span[0]

    def __lt__(self, other):
        return self.span[0] < other.span[0]

    def overlaps(self, other):
        return max(self.span[0], other.span[0]) <= min(self.span[1], other.span[1])


__all__ = ["CodeRegion"]
