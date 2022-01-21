"""This module implements LWW Element Set.

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

"""
import enum
from typing import Generic, TypeVar

from ..utils.timestamp import timestamp_now


T = TypeVar("T")


class Bias(enum.Enum):
    """Indicates if LwwElementSet is biased towards adds or removals."""

    ADDS = enum.auto()
    REMOVES = enum.auto()


class LwwElementSet(Generic[T]):
    """LWW-Element-Set is a Conflict-free Replicated Data Type."""

    def __init__(
        self,
        bias: Bias = Bias.ADDS,
        initial_add_timestamps: dict[T, int] = None,
        initial_remove_timestamps: dict[T, int] = None,
    ):
        self.bias = bias
        self.add_timestamps = initial_add_timestamps or {}
        self.remove_timestamps = initial_remove_timestamps or {}

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
            if Bias.ADDS:
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

    def merge(self, other: "LwwElementSet[T]") -> "LwwElementSet[T]":
        """Merges two instances of the structure.

        Merging two replicas of the LWW-Element-Set consists of taking
        the union of the add sets and the union of the remove sets.

        When timestamps are equal, the "bias" of the LWW-Element-Set
        comes into play. A LWW-Element-Set can be biased towards adds or
        removals.

        The advantage of LWW-Element-Set over 2P-Set is that, unlike 2P-Set,
        LWW-Element-Set allows an element to be reinserted after having been removed.
        """
        assert self.bias == other.bias, "Merged sets should have same bias."

        merged_add_timestamps = {**self.add_timestamps}
        merged_remove_timestamps = {**self.remove_timestamps}

        for element, timestamp in other.add_timestamps.items():
            merged_add_timestamps[element] = timestamp

        for element, timestamp in other.remove_timestamps.items():
            merged_remove_timestamps[element] = timestamp

        merged_set: LwwElementSet[T] = LwwElementSet(
            bias=self.bias,
            initial_add_timestamps=merged_add_timestamps,
            initial_remove_timestamps=merged_remove_timestamps,
        )

        return merged_set
