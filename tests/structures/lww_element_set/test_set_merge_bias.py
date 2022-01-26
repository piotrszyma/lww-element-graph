from freezegun import freeze_time

from lww_element_graph.structures.lww_element_set import Bias, LwwElementSet


def test_merge_bias_removes():
    # Arrange.
    first_lww: LwwElementSet[str] = LwwElementSet(bias=Bias.REMOVES)

    second_lww: LwwElementSet[str] = LwwElementSet(bias=Bias.REMOVES)

    with freeze_time() as frozen_time:
        second_lww.add("abc")

        frozen_time.tick()

        # Simulate element added to one set and removed from other at one moment.
        first_lww.add("abc")
        second_lww.remove("abc")

    # Act.
    merged_lww = first_lww.merge(second_lww)

    # Assert.
    assert (
        merged_lww.lookup("abc") is False
    ), "Element should not be present if bias = REMOVES"


def test_merge_bias_adds():
    # Arrange.
    first_lww: LwwElementSet[str] = LwwElementSet(bias=Bias.ADDS)
    second_lww: LwwElementSet[str] = LwwElementSet(bias=Bias.ADDS)

    with freeze_time() as frozen_time:
        second_lww.add("abc")

        frozen_time.tick()

        # Simulate element added to one set and removed from other at one moment.
        first_lww.add("abc")
        second_lww.remove("abc")

    # Act.
    merged_lww = first_lww.merge(second_lww)

    # Assert.
    assert merged_lww.lookup("abc") is True
