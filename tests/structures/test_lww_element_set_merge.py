from lww_element_graph.structures.lww_element_set import LwwElementSet


def test_merge_lww_element_sets():
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
