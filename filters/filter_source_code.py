import os
import re
from models import CodeRegion
from queue import LifoQueue


class FilterSourceCode:
    """A class that parses code from a given string"""

    def __init__(self, data_source: str):
        self._data = data_source
        self._patterns: {str: re.Pattern} = {}
        self._pattern_options = []
        self._resource_path = os.path.join("..", "resources", "Java_CodeDB.txt")

        self._loadRegEx()

    def _loadRegEx(self):
        """Loads regex expressions from text file"""
        with open(self._resource_path, "r") as file:
            for line in file:
                parts = line.split(",")
                if len(parts) < 2:
                    raise RuntimeError("The input file is invalid")

                self._patterns[parts[0]] = parts[1].strip()
                option = True if len(parts) == 3 else False
                self._pattern_options.append(option)

    def filter(self) -> [CodeRegion]:
        """Filters the data source and returns a list of filtered java expressions """
        regions = []

        for (region_type, pattern), do_match in zip(self._patterns.items(), self._pattern_options):
            for match in re.finditer(pattern, self._data):
                region = CodeRegion(
                    region_type=region_type,
                    span=match.span(),
                    source_code=match.group()
                )
                if do_match:
                    region = self._findMatch(region) or region

                regions.append(region)

        self._merge_regions(regions)
        return regions

    def _findMatch(self, region: CodeRegion) -> CodeRegion | None:
        """Finds the matching enclosing parenthesis given the input expression
        :param region: The code region to match for
        """

        brace_stack = LifoQueue()
        brace_stack.put("{")
        original_span = region.span
        search_region = self._data[original_span[1]:]
        for index, char in enumerate(search_region):
            if char == "}":
                brace_stack.get()

            elif char == "{":
                brace_stack.put(char)

            if brace_stack.empty():
                matched_region = CodeRegion(
                    region_type=region.type,
                    span=(original_span[0], original_span[1]+index+1),
                    source_code=region.source_code + search_region[:index+1]
                )
                return matched_region

        return None

    def _merge_regions(self, regions: [CodeRegion]):
        regions.sort()
        i = 0
        while i < len(regions) - 1:
            lhs = regions[i]
            rhs = regions[i + 1]
            if lhs.overlaps(rhs):
                merged_span = (
                    min(lhs.span[0], rhs.span[0]),
                    max(lhs.span[1], rhs.span[1])
                )
                merged_code = self._data[merged_span[0]:merged_span[1]]
                merged_region = CodeRegion(
                    lhs.type,
                    merged_span,
                    merged_code
                )
                regions[i] = merged_region
                del regions[i + 1]

            else:
                i += 1



if __name__ == "__main__":
    with open("../demo/demo_report.txt", "r") as file:
        content = file.read()
        source_code_filter = FilterSourceCode(content)
        results = source_code_filter.filter()
        results.sort()
        print(results)


__all__ = ["FilterSourceCode"]
