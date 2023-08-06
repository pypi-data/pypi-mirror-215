from collections import Counter
from collections.abc import Iterator
from typing import Self

from pydantic import Field

from .components import Rule, StatuteSerialCategory
from .names import NamedRules
from .serials import SerializedRules


def extract_rules(text: str) -> Iterator[Rule]:
    """If text contains [serialized][serial-pattern] (e.g. _Republic Act No. 386_)
    and [named][named-pattern] rules (_the Civil Code of the Philippines_),
    extract the [`Rules`][rule-model] into their canonical serial variants.

    Examples:
        >>> text = "The Civil Code of the Philippines, the old Spanish Civil Code; Rep Act No. 386"
        >>> list(extract_rules(text)) # get all rules
        [ra 386, ra 386, spain civil]

    Args:
        text (str): Text to search for statute patterns.

    Yields:
        Iterator[Rule]: Serialized Rules and Named Rule patterns
    """  # noqa: E501
    yield from SerializedRules.extract_rules(text)
    yield from NamedRules.extract_rules(text)


def extract_rule(text: str) -> Rule | None:
    """Thin wrapper over [`extract_rules()`][extract-rules]. If text contains a
    matching [`Rule`][rule-model], get the first one found.

    Examples:
        >>> text = "The Civil Code of the Philippines, the old Spanish Civil Code; Rep Act No. 386"
        >>> extract_rule(text)  # get the first matching rule
        ra 386

    Args:
        text (str): Text to search for statute patterns.

    Returns:
        Rule | None: The first Rule found, if it exists
    """  # noqa: E501
    try:
        return next(extract_rules(text))
    except StopIteration:
        return None


class CountedRule(Rule):
    """Based on results from [`extract_rules()`][extract-rules], get count of each
    unique rule found."""

    mentions: int = Field(...)

    def __repr__(self) -> str:
        return f"{self.cat} {self.id}: {self.mentions}"

    @classmethod
    def from_source(cls, text: str) -> Iterator[Self]:
        """Detect counted rules from source `text`.

        Examples:
            >>> text = "The Civil Code of the Philippines, the old Spanish Civil Code; Rep Act No. 386"
            >>> results = list(CountedRule.from_source(text))
            >>> results
            [ra 386: 2, spain civil: 1]
            >>> results[0] == CountedRule(cat=StatuteSerialCategory('ra'),id='386', mentions=2)
            True
            >>> results[1] == CountedRule(cat=StatuteSerialCategory('spain'),id='civil', mentions=1)
            True

        Args:
            text (str): Legalese containing statutory rules in various formats.

        Yields:
            Iterator[Self]: Each counted rule found.
        """  # noqa: E501
        rules = extract_rules(text)
        for k, v in Counter(rules).items():
            yield cls(cat=k.cat, id=k.id, mentions=v)

    @classmethod
    def from_repr_format(cls, repr_texts: list[str]) -> Iterator[Self]:
        """Generate their pydantic counterparts from `<cat> <id>: <mentions>` format.

        Examples:
            >>> repr_texts = ['ra 386: 2', 'spain civil: 1']
            >>> results = list(CountedRule.from_repr_format(repr_texts))
            >>> results
            [ra 386: 2, spain civil: 1]
            >>> results[0].cat
            'ra'
            >>> results[0].id
            '386'
            >>> results[0].mentions
            2
            >>> str(results[0])
            'Republic Act No. 386'
            >>> repr(results[0])
            'ra 386: 2'


        Args:
            texts (str): list of texts having `__repr__` format of a `CountedRule`

        Yields:
            Iterator[Self]: Instances of CountedRule
        """
        for text in repr_texts:
            counted_bits = text.split(":")
            if len(counted_bits) == 2:
                statute_bits = counted_bits[0].split()
                mentions = counted_bits[1]
                is_cat_id = len(statute_bits) == 2
                is_digit_bit = mentions.strip().isdigit()
                if is_cat_id and is_digit_bit:
                    if cat := StatuteSerialCategory(statute_bits[0]):
                        yield cls(cat=cat, id=statute_bits[1], mentions=int(mentions))
