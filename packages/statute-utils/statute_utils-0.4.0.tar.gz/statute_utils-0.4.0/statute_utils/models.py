import re
from collections.abc import Iterator
from re import Pattern

from pydantic import Field

from .components import BaseCollection, BasePattern, Rule, StatuteSerialCategory, stx
from .recipes import split_digits


class NamedPattern(BasePattern):
    """A [`Rule`][rule-model] can be extracted from a `NamedPattern`"""

    name: str
    regex_base: str
    rule: Rule

    @property
    def regex(self) -> str:
        return stx(rf"(?P<{self.group_name}>{self.regex_base})")

    @property
    def group_name(self) -> str:
        return self.rule.slug


class NamedPatternCollection(BaseCollection):
    """Each named legal title, not falling under the SerialNames Patterns,
    will also have its own manually crafted regex string. Examples include
    'the Spanish Civil Code' or the '1987 Constitution' or the
    'Code of Professional Responsibility'.
    """

    collection: list[NamedPattern]

    def extract_rules(self, text: str) -> Iterator[Rule]:
        for m in self.pattern.finditer(text):
            for named in self.collection:
                if m.lastgroup == named.group_name:
                    yield named.rule


class SerialPattern(BasePattern):
    """A [`Rule`][rule-model] can be extracted from a `SerialPattern`. The word _serial_
    is employed because the documents representing rules are numbered consecutively.

    Each serial pattern refers to a [`Statute Category`][statute-category-model],
    e.g. `RA`, `CA`, etc. matched with a
    [`Serial Identifier`][statute-serial-identifier].

    Since a `SerialPattern` inherits from a [BasePattern][base-pattern], it includes
    other fields declared in the latter model: `matches` and `excludes` bringing the
    total number of fields to 5, viz.:

    Field | Description | Example
    --:|:--|:--
    `cat` | [`Statute Category`][statute-category-model] | StatuteSerialCategory.RepublicAct
    `regex_bases` | How do we pattern the category name? | ["r.a. no.", "Rep. Act. No."]
    `regex_serials` | What digits are allowed | ["386", "11114"]
    `matches` | Usable in parametized tests to determine whether the pattern declared matches the samples | ["Republic Act No. 7160", "R.A. 386 and 7160" ]
    `excludes` | Usable in parametized tests to determine that the full pattern will not match | ["Republic Act No. 7160:", "RA 9337-"]
    """  # noqa: E501

    cat: StatuteSerialCategory = Field(
        ...,
        title="Statute Serial Category",
        description=(
            "A type of rule from the taxonomy enumerated under StatuteSerialCategory."
        ),
    )
    regex_bases: list[str] = Field(
        ...,
        title="Prefix Label in Regex",
        description=(
            "There are too many ways to express a category name. There is a"
            " need to generate various regex strings which, when combined with"
            " the serial, can qualify for a serial rule."
        ),
    )
    regex_serials: list[str] = Field(
        ...,
        title="Serial Identifiers in Regex",
        description=(
            "The possible values of serial numbers to be matched with the regex_bases."
        ),
    )

    @property
    def lines(self) -> Iterator[str]:
        """Each regex string produced matches the serial rule. Note the line break
        needs to be retained so that when printing `@regex`, the result is organized.
        """
        for base in self.regex_bases:
            for idx in self.regex_serials:
                yield rf"""({base}\s*{idx})
                """

    @property
    def group_name(self) -> str:
        return rf"serial_{self.cat.name}"

    @property
    def regex(self) -> str:
        return rf"(?P<{self.group_name}>{r'|'.join(self.lines)})"

    @property
    def digits_in_match(self) -> Pattern:
        return re.compile(r"|".join(self.regex_serials))


class SerialPatternCollection(BaseCollection):
    """Each category-based, serial-numbered, legal title will have a
    regex string, e.g. Republic Act is a category, a serial number for
    this category is 386 representing the Philippine Civil Code."""

    collection: list[SerialPattern]

    def extract_rules(self, text: str) -> Iterator[Rule]:
        """Each `m`, a python Match object, represents a
        serial pattern category with possible ambiguous identifier found.

        So running `m.group(0)` should yield the entire text of the
        match which consists of (a) the definitive category;
        and (b) the ambiguous identifier.

        The identifier is ambiguous because it may be a compound one,
        e.g. 'Presidential Decree No. 1 and 2'. In this case, there
        should be 2 matches produced not just one.

        This function splits the identifier by commas `,` and the
        word `and` to get the individual component identifiers.
        """
        for match in self.pattern.finditer(text):
            for sp in self.collection:
                if match.lastgroup == sp.group_name:
                    if candidates := sp.digits_in_match.search(match.group(0)):
                        for d in split_digits(candidates.group(0)):
                            yield Rule(cat=sp.cat, id=d)
