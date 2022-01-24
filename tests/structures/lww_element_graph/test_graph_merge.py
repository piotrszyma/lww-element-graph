from freezegun import freeze_time
from more_itertools import first

from lww_element_graph.structures.lww_element_graph import LwwElementGraph


def test_merge_vertices_values_set_in_the_same_time_replica_which_is_merged_wins():
    # Arrange.
    first_replica = LwwElementGraph()
    second_replica = LwwElementGraph()

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
    # TODO(szyma): Make it result in same merged replica.
    assert first_replica.merge(second_replica).get_vertex_value("1") == 456
    assert second_replica.merge(first_replica).get_vertex_value("1") == 123

