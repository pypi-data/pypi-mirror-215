"""
Context handlers.
"""
import re
import textwrap
from typing import List, Iterator, Optional

from tabulate import tabulate


class UniqueString(str):
    pass


CONTENT_START = UniqueString("content start")
EOL = "\n"
SPACE_CHARS = re.compile(r"\s+")
WRAP_REGEXP = re.compile(r"(\s*)(?=\S)([\s\S]+?)(?<=\S)(\s*)", re.M)


def is_content_start(value: str):
    return isinstance(value, UniqueString) and value is CONTENT_START


class SubContext:
    def __init__(self):
        self.body: List[str] = []
        self.ensure_eol_count = 0

    @property
    def content(self) -> List[str]:
        return self.body

    def _iter_reverse_char(self) -> Iterator[str]:
        for value in reversed(self.content):
            yield from reversed(value)

        yield CONTENT_START

    def _count_missing_eol(self) -> int:
        """
        Add required number of EOL characters.
        Avoids adding EOL at the beginning of the content.
        Ignores spaces when traversing the content.
        """
        missing_count = self.ensure_eol_count
        for value in self._iter_reverse_char():
            if is_content_start(value):
                missing_count = 0
            if missing_count <= 0 or SPACE_CHARS.fullmatch(value) is None:
                break
            if value == EOL:
                missing_count -= 1

        return max(0, missing_count)

    def ensure_eol(self, count: int = 1):
        self.ensure_eol_count = max(self.ensure_eol_count, count)

    def add(self, value: str):
        missing_eol = self._count_missing_eol()
        if missing_eol > 0:
            self.content.append(EOL * missing_eol)

        self.content.append(value)
        self.ensure_eol_count = 0

    def make(self) -> str:
        return "".join(self.content)


class WrappedContext(SubContext):
    def __init__(self, prefix, suffix: Optional[str] = None, wrap_empty=False):
        super().__init__()
        self.prefix = prefix
        self.suffix = suffix if suffix is not None else prefix
        self.wrap_empty = wrap_empty

    def make(self):
        content = super().make()
        match = WRAP_REGEXP.fullmatch(content)
        if match is None:
            # The expression has no match only when there is no non-space character.
            if self.wrap_empty:
                return f"{self.prefix}{content}{self.suffix}"
            return content

        # We need to make sure the emphasis mark is near a non-space char,
        # but we want to preserve the existing spaces.
        prefix_space, text, suffix_space = match.groups()
        return f"{prefix_space}{self.prefix}{text}{self.suffix}{suffix_space}"


class CommaSeparatedContext(SubContext):
    def __init__(self, sep: str = ", "):
        super().__init__()
        self.sep = sep
        self.body: List[List[str]] = []

        self.is_parameter = False

    def enter_parameter(self):
        self.is_parameter = True
        self.body.append([])

    def exit_parameter(self):
        self.is_parameter = False

    @property
    def content(self):
        assert self.is_parameter
        return self.body[-1]

    def make(self):
        return self.sep.join(["".join(item) for item in self.body])


class TableContext(SubContext):
    def __init__(self):
        super().__init__()
        self.body: List[List[List[str]]] = []
        self.headers: List[List[List[str]]] = []
        self._active_output: Optional[List[List[List[str]]]] = None

        self.is_row = False
        self.is_entry = False

    @property
    def active_output(self) -> List[List[List[str]]]:
        assert self._active_output is not None
        return self._active_output

    @property
    def content(self):
        assert self.is_entry
        return self.active_output[-1][-1]

    def enter_head(self):
        assert self._active_output is None
        self._active_output = self.headers

    def exit_head(self):
        assert self._active_output is self.headers
        self._active_output = None

    def enter_body(self):
        assert self._active_output is None
        self._active_output = self.body

    def exit_body(self):
        assert self._active_output is self.body
        self._active_output = None

    def enter_row(self):
        self.active_output.append([])
        self.is_row = True

    def exit_row(self):
        assert self.is_row
        self.is_row = False

    def enter_entry(self):
        assert self.is_row
        self.is_entry = True
        self.active_output[-1].append([])
        self.ensure_eol_count = 0

    def exit_entry(self):
        assert self.is_entry
        self.is_entry = False

    @staticmethod
    def make_row(row):
        return ["".join(entries).replace("\n", "<br/>") for entries in row]

    def make(self):
        content = [*self.headers, *self.body]
        assert len(content) > 0, "Empty table"
        headers = self.make_row(content[0])
        body = list(map(self.make_row, content[1:]))
        return tabulate(body, headers=headers, tablefmt="github")


class IndentContext(SubContext):
    def __init__(self, prefix, only_first=False):
        super().__init__()
        if only_first:
            self.prefix = " " * len(prefix)
            self.first_prefix = prefix
        else:
            self.prefix = prefix
            self.first_prefix = None

    def make(self):
        content = textwrap.indent(super().make(), self.prefix)
        if self.first_prefix is None:
            return content
        return content.replace(self.prefix, self.first_prefix, 1)
