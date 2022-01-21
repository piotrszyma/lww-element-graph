from lww_element_graph.structures.lww_element_set import LwwElementSet


def test_insert():
    # Arrange.
    lww: LwwElementSet[str] = LwwElementSet()

    # Act.
    lww.add("abc")

    # Assert.
    assert lww.lookup("abc") is True


def test_remove():
    # Arrange.
    lww: LwwElementSet[str] = LwwElementSet()
    lww.add("abc")

    # Act.
    lww.remove("abc")

    # Assert.
    assert lww.lookup("abc") is False
