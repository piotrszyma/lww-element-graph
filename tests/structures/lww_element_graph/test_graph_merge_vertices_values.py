from freezegun import freeze_time

from lww_element_graph.structures.lww_element_graph import LwwElementGraph


def test_merge_vertices_values():
    # Arrange.
    first_replica: LwwElementGraph[int] = LwwElementGraph()
    second_replica: LwwElementGraph[int] = LwwElementGraph()

    first_replica.add_vertex("1")
    first_replica.set_vertex_value("1", 456)
    second_replica.add_vertex("2")
    second_replica.set_vertex_value("2", 123)

    # Act.
    merged_replica = first_replica.merge(second_replica)

    # Assert.
    assert merged_replica.has_vertex("1") is True
    assert merged_replica.has_vertex("2") is True
    assert merged_replica.get_vertex_value("1") == 456
    assert merged_replica.get_vertex_value("2") == 123


def test_later_first_vertex_value_takes_precedence():
    # Arrange.
    first_replica: LwwElementGraph[int] = LwwElementGraph()
    second_replica: LwwElementGraph[int] = LwwElementGraph()

    first_replica.add_vertex("1")
    second_replica.add_vertex("1")
    first_replica.set_vertex_value("1", 123)
    second_replica.set_vertex_value("1", 456)

    # Act.
    merged_replica = first_replica.merge(second_replica)

    # Assert.
    assert (
        merged_replica.get_vertex_value("1") == 456
    ), "Value set later should take recedence."


def test_later_second_vertex_value_takes_precedence():
    # Arrange.
    first_replica: LwwElementGraph[int] = LwwElementGraph()
    second_replica: LwwElementGraph[int] = LwwElementGraph()

    first_replica.add_vertex("1")
    second_replica.add_vertex("1")
    second_replica.set_vertex_value("1", 456)
    first_replica.set_vertex_value("1", 123)

    # Act.
    merged_replica = first_replica.merge(second_replica)

    # Assert.
    assert (
        merged_replica.get_vertex_value("1") == 123
    ), "Value set later should take recedence."


def test_merge_vertices_values_set_in_the_same_time_replica_which_is_merged_wins():
    """Edge case - two replicas assigned different value at the same time."""
    # Arrange.
    first_replica: LwwElementGraph[int] = LwwElementGraph()
    second_replica: LwwElementGraph[int] = LwwElementGraph()

    with freeze_time() as frozen_time:
        first_replica.add_vertex("1")
        first_replica.add_vertex("2")
        first_replica.add_edge("1", "2")

        second_replica.add_vertex("1")
        second_replica.add_vertex("2")
        second_replica.add_edge("1", "2")

        frozen_time.tick()

        # Vertex value set at the same time.
        first_replica.set_vertex_value("1", 456)
        second_replica.set_vertex_value("1", 123)

    # Act & Assert.
    assert first_replica.merge(second_replica).get_vertex_value("1") == 456
    assert second_replica.merge(first_replica).get_vertex_value("1") == 456
