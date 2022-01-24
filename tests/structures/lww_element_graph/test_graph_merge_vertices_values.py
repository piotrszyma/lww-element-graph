from freezegun import freeze_time

from lww_element_graph.structures.lww_element_graph import LwwElementGraph
from lww_element_graph.structures.lww_element_set import Bias


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
    assert merged_replica.get_vertex_value("1") == 456


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
    assert merged_replica.get_vertex_value("1") == 123


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
