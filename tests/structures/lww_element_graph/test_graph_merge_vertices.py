from lww_element_graph.structures.lww_element_graph import LwwElementGraph


def test_later_add_takes_precendence():
    # Arrange.
    first_replica = LwwElementGraph()
    second_replica = LwwElementGraph()

    first_replica.add_vertex("1")
    first_replica.remove_vertex("1")
    second_replica.add_vertex("1")

    # Act.
    merged_replica = first_replica.merge(second_replica)

    # Assert.
    assert merged_replica.has_vertex("1") is True


def test_later_remove_takes_precendence():
    # Arrange.
    first_replica = LwwElementGraph()
    second_replica = LwwElementGraph()

    first_replica.add_vertex("1")
    second_replica.add_vertex("1")
    second_replica.remove_vertex("1")

    # Act.
    merged_replica = first_replica.merge(second_replica)

    # Assert.
    assert merged_replica.has_vertex("1") is False


def test_merge_after_vertex_removal_removes_connected_edges():
    # Arrange.
    first_replica = LwwElementGraph()
    first_replica.add_vertex("1")
    first_replica.add_vertex("2")
    first_replica.add_edge("1", "2")

    second_replica = LwwElementGraph()
    second_replica.add_vertex("1")
    second_replica.add_vertex("2")
    second_replica.add_edge("1", "2")
    second_replica.remove_edge("1", "2")
    second_replica.remove_vertex("1")

    first_replica.add_vertex("3")
    first_replica.add_edge("1", "3")

    # Act.
    merged_replica = first_replica.merge(second_replica)

    # Assert.
    assert len(tuple(merged_replica.edges.values())) == 0
    assert len(tuple(merged_replica.vertices.values())) == 2
    assert merged_replica.has_vertex("1") is False
    assert merged_replica.has_vertex("2") is True
    assert merged_replica.has_vertex("3") is True
    assert merged_replica.has_edge("1", "2") is False
    assert merged_replica.has_edge("1", "3") is False


def test_merge_after_last_vertex_removal_merge_has_vertex_removed():
    # Arrange.
    first_replica = LwwElementGraph()
    first_replica.add_vertex("1")

    second_replica = LwwElementGraph()
    second_replica.add_vertex("1")

    # Last operation was removal.
    # It should result in lack of this item in merged_replica.
    first_replica.remove_vertex("1")

    # Act.
    merged_replica = first_replica.merge(second_replica)

    # Assert.
    assert merged_replica.has_vertex("1") is False
