from lww_element_graph.structures.lww_element_set import LwwElementSet


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


def test_later_add_timestamp_takes_precendence():
    # Arrange.
    first_lww: LwwElementSet[str] = LwwElementSet()
    second_lww: LwwElementSet[str] = LwwElementSet()

    first_lww.add("abc")
    first_lww.remove("abc")
    # Last operation was add. Element should be in merged set.
    second_lww.add("abc")

    # Act.
    merged_lww = first_lww.merge(second_lww)

    # Assert.
    assert merged_lww.lookup("abc") is True


def test_later_remove_timestamp_takes_precendence():
    # Arrange.
    first_lww: LwwElementSet[str] = LwwElementSet()
    second_lww: LwwElementSet[str] = LwwElementSet()

    first_lww.add("abc")
    second_lww.add("abc")
    # Last operation was remove. Element should not be in merged set.
    second_lww.remove("abc")

    # Act.
    merged_lww = first_lww.merge(second_lww)

    # Assert.
    assert merged_lww.lookup("abc") is False
