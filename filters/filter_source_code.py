import os
import re
from models import CodeRegion


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

        return regions

    def _findMatch(self, region: CodeRegion) -> CodeRegion | None:
        """Finds the matching enclosing parenthesis given the input expression
        :param region: The code region to match for
        """
        ...

    def _merge_regions(self) -> [CodeRegion]:
        ...


if __name__ == "__main__":
    with open("../demo/demo_report.txt", "r") as file:
        content = file.read()

        source_code_filter = FilterSourceCode(content)
        print(source_code_filter.filter())

__all__ = ["FilterSourceCode"]
