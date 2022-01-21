"""This module contains implementation of a LWW-Element-Set.

Notes on LWW-Element-Set from Wikipedia:

# 2P-Set

```
payload set A, set R
    initial ∅, ∅
query lookup(element e) : boolean b
    let b = (e ∈ A ∧ e ∉ R)
update add(element e)
    A := A ∪ {e}
update remove(element e)
    pre lookup(e)
    R := R ∪ {e}
compare (S, T) : boolean b
    let b = (S.A ⊆ T.A ∧ S.R ⊆ T.R)
merge (S, T) : payload U
    let U.A = S.A ∪ T.A
    let U.R = S.R ∪ T.R
```

Two G-Sets (grow-only sets) are combined to create the 2P-set.
With the addition of a remove set (called the "tombstone" set),
elements can be added and also removed.

Once removed, an element cannot be re-added; that is, once an element e
is in the tombstone set, query will never again return True for that element.
The 2P-set uses "remove-wins" semantics, so remove(e) takes precedence over add(e).

# LWW-Element-Set

LWW-Element-Set is similar to 2P-Set in that it consists of an "add set" and
a "remove set", with a timestamp for each element.

Elements are added to an LWW-Element-Set by inserting
the element into the add set, with a timestamp.

Elements are removed from the LWW-Element-Set by being added to the remove set,
again with a timestamp.

An element is a member of the LWW-Element-Set if it is in the add set,
and either not in the remove set, or in the remove set but with an earlier timestamp
than the latest timestamp in the add set.

Merging two replicas of the LWW-Element-Set consists
of taking the union of the add sets and the union of the remove sets.
When timestamps are equal, the "bias" of the LWW-Element-Set comes into play.
A LWW-Element-Set can be biased towards adds or removals.

The advantage of LWW-Element-Set over 2P-Set is that, unlike 2P-Set,
LWW-Element-Set allows an element to be reinserted after having been removed.

For more details about this structure, search for "Conflict-free replicated data type".
"""
import enum
from typing import Generic, Iterable, TypeVar

from ..utils.timestamp import timestamp_now

T = TypeVar("T")
Timestamp = int


class Bias(enum.Enum):
    """Indicates if LwwElementSet is biased towards adds or removals."""

    ADDS = enum.auto()
    REMOVES = enum.auto()


class LwwElementSet(Generic[T]):
    """LWW-Element-Set is a Conflict-free Replicated Data Type."""

    def __init__(
        self,
        bias: Bias = Bias.ADDS,
        initial_add_timestamps: dict[T, Timestamp] = None,
        initial_remove_timestamps: dict[T, Timestamp] = None,
    ):
        self.bias = bias
        self.add_timestamps = initial_add_timestamps or {}
        self.remove_timestamps = initial_remove_timestamps or {}

    def __repr__(self):
        add_elements = set(self.add_timestamps.keys())
        remove_elements = set(self.remove_timestamps.keys())
        return f"<LwwElementSet add={add_elements} remove={remove_elements}>"

    def lookup(self, element: T) -> bool:
        """Returns boolean indicating if `value` is a member of structure.

        An element is a member of the LWW-Element-Set if it is in the add set,
        and either not in the remove set, or in the remove set but with an
        earlier timestamp than the latest timestamp in the add set.

        When timestamps are equal, the "bias" of the LWW-Element-Set
        comes into play. A LWW-Element-Set can be biased towards adds or
        removals.
        """
        is_in_add_set = element in self.add_timestamps
        is_in_remove_set = element in self.remove_timestamps

        if not is_in_add_set:
            return False

        if is_in_add_set and not is_in_remove_set:
            return True

        timestamp_add_set = self.add_timestamps[element]
        timestamp_remove_set = self.remove_timestamps[element]

        if timestamp_add_set == timestamp_remove_set:
            if self.bias == Bias.ADDS:
                return True
            else:
                return False

        return timestamp_add_set > timestamp_remove_set

    def add(self, element: T) -> None:
        """Adds element to the structure.

        Elements are added to an LWW-Element-Set by inserting
        the element into the add set, with a timestamp.
        """
        self.add_timestamps[element] = timestamp_now()

    def remove(self, element: T) -> None:
        """Removes element from the structure.

        Elements are removed from the LWW-Element-Set by being added
        to the remove set, again with a timestamp.
        """
        self.remove_timestamps[element] = timestamp_now()

    def _merge_timestamps(
        self, first_to_merge: dict[T, Timestamp], second_to_merge: dict[T, Timestamp]
    ) -> dict[T, Timestamp]:
        """Merges two dicts of elements mapped to timestamps.

        If element is present in only one of dicts, it is placed in merged dict.
        If element is present in both dicts, the later (bigger) timestamp is placed
        in merged dict.
        """

        elements = {*first_to_merge.keys(), *second_to_merge.keys()}
        merged: dict[T, Timestamp] = {}

        for element in elements:
            first_timestamp = first_to_merge.get(element)
            second_timestamp = second_to_merge.get(element)

            if first_timestamp is not None and second_timestamp is not None:
                merged[element] = max(first_timestamp, second_timestamp)
            elif second_timestamp is not None:
                merged[element] = second_timestamp
            else:
                assert first_timestamp is not None
                merged[element] = first_timestamp

        return merged

    def merge(self, other: "LwwElementSet[T]") -> "LwwElementSet[T]":
        """Merges two instances of the structure.

        Merging two replicas of the LWW-Element-Set consists of taking
        the union of the add sets and the union of the remove sets.
        """
        assert self.bias == other.bias, "Merged sets should have same bias."

        merged_add_timestamps = self._merge_timestamps(
            self.add_timestamps, other.add_timestamps
        )

        merged_remove_timestamps = self._merge_timestamps(
            self.remove_timestamps, other.remove_timestamps
        )

        merged_set: LwwElementSet[T] = LwwElementSet(
            bias=self.bias,
            initial_add_timestamps=merged_add_timestamps,
            initial_remove_timestamps=merged_remove_timestamps,
        )

        return merged_set

    def values(self) -> Iterable[T]:
        """Returns iterator over members of structure."""
        elements_in_add = self.add_timestamps.keys()
        for element in elements_in_add:
            if self.lookup(element):
                yield element

    def __contains__(self, element: T) -> bool:
        """Wrapper over lookup to support in operator."""
        return self.lookup(element)
