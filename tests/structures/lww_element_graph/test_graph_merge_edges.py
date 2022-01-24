from lww_element_graph.structures.lww_element_graph import LwwElementGraph


def test_merge_edges():
    # Arrange.
    first_replica: LwwElementGraph[int] = LwwElementGraph()
    second_replica: LwwElementGraph[int] = LwwElementGraph()

    first_replica.add_vertex("1")
    first_replica.add_vertex("2")
    first_replica.add_vertex("3")
    first_replica.add_vertex("4")
    first_replica.add_edge("1", "2")
    first_replica.add_edge("2", "3")
    first_replica.add_edge("2", "4")
    second_replica.add_vertex("1")
    second_replica.add_vertex("2")
    second_replica.add_vertex("3")
    second_replica.add_vertex("4")
    first_replica.add_edge("1", "4")
    first_replica.add_edge("1", "3")

    # Act.
    merged_replica = first_replica.merge(second_replica)

    # Assert.
    assert set(merged_replica.vertices.values()) == {"1", "2", "3", "4"}
    assert set(merged_replica.edges.values()) == {
        frozenset(("1", "3")),
        frozenset(("2", "3")),
        frozenset(("2", "1")),
        frozenset(("4", "2")),
        frozenset(("4", "1")),
    }
