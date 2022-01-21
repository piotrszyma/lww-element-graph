from freezegun import freeze_time

from lww_element_graph.structures.lww_element_set import Bias, LwwElementSet


def test_merge():
    # Arrange.
    first_lww: LwwElementSet[str] = LwwElementSet()
    first_lww.add("abc")
    first_lww.add("def")

    second_lww: LwwElementSet[str] = LwwElementSet()
    second_lww.add("abc")
    second_lww.add("ghi")

    # Act.
    merged_lww = first_lww.merge(second_lww)

    # Assert.
    assert merged_lww.lookup("abc") is True
    assert merged_lww.lookup("def") is True
    assert merged_lww.lookup("ghi") is True


def test_merge_remove_previously_added():
    # Arrange.
    first_lww: LwwElementSet[str] = LwwElementSet()
    first_lww.add("abc")

    second_lww: LwwElementSet[str] = LwwElementSet()
    second_lww.add("abc")

    # Last operation was removal.
    # It should result in lack of this item in merged_lww.
    first_lww.remove("abc")

    # Act.
    merged_lww = first_lww.merge(second_lww)

    # Assert.
    assert merged_lww.lookup("abc") is False


def test_bias_towards_adds_should_be_present_in_merged():
    # Arrange.
    first_lww: LwwElementSet[str] = LwwElementSet(bias=Bias.ADDS)
    second_lww: LwwElementSet[str] = LwwElementSet()

    with freeze_time() as frozen_time:
        # Element was present only in first.
        first_lww.add("abc")

        # Time moves.
        frozen_time.tick()

        # At the same moment,
        # element was removed from first_lww and added to second_lww.
        first_lww.remove("abc")
        second_lww.add("abc")

    # Act.
    merged_lww = first_lww.merge(second_lww)

    # Assert.
    assert merged_lww.lookup("abc") is True


def test_bias_towards_removes_should_not_be_present_in_merged():
    # Arrange.
    first_lww: LwwElementSet[str] = LwwElementSet(bias=Bias.REMOVES)
    second_lww: LwwElementSet[str] = LwwElementSet(bias=Bias.REMOVES)

    # At the same moment, element was removed from first_lww and added to second_lww.
    with freeze_time() as frozen_time:
        # Element was present only in first.
        first_lww.add("abc")

        # Time moves.
        frozen_time.tick()

        # At the same moment,
        # element was removed from first_lww and added to second_lww.
        first_lww.remove("abc")
        second_lww.add("abc")

    # Act.
    merged_lww = first_lww.merge(second_lww)

    # Assert.
    assert merged_lww.lookup("abc") is False


def test_later_add_timestamp_takes_precendence():
    # Arrange.
    first_lww: LwwElementSet[str] = LwwElementSet(bias=Bias.REMOVES)
    second_lww: LwwElementSet[str] = LwwElementSet(bias=Bias.REMOVES)

    first_lww.add("abc")
    first_lww.remove("abc")
    second_lww.add("abc")

    # Act.
    merged_lww = first_lww.merge(second_lww)

    # Assert.
    assert merged_lww.lookup("abc") is True


def test_later_remove_timestamp_takes_precendence():
    # Arrange.
    first_lww: LwwElementSet[str] = LwwElementSet(bias=Bias.REMOVES)
    second_lww: LwwElementSet[str] = LwwElementSet(bias=Bias.REMOVES)

    first_lww.add("abc")
    first_lww.remove("abc")
    second_lww.add("abc")
    second_lww.remove("abc")

    # Act.
    merged_lww = first_lww.merge(second_lww)

    # Assert.
    assert merged_lww.lookup("abc") is False
