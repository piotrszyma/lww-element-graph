from lww_element_graph.structures.lww_element_graph import LwwElementGraph


def test_merge_with_removed_vertex():
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
    assert merged_replica.has_vertex("1") is False
    assert merged_replica.has_vertex("2") is True
    assert merged_replica.has_vertex("3") is True
    assert merged_replica.has_edge("1", "2") is False
    assert merged_replica.has_edge("1", "3") is False
