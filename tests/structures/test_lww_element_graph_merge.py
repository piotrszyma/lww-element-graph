from freezegun import freeze_time
from more_itertools import first
from lww_element_graph.structures.lww_element_graph import LwwElementGraph
from lww_element_graph.structures.lww_element_set import Bias


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
    assert len(tuple(merged_replica.edges.values())) == 0
    assert len(tuple(merged_replica.vertexes.values())) == 2
    assert merged_replica.has_vertex("1") is False
    assert merged_replica.has_vertex("2") is True
    assert merged_replica.has_vertex("3") is True
    assert merged_replica.has_edge("1", "2") is False
    assert merged_replica.has_edge("1", "3") is False


def test_merge_remove_previously_added():
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


def test_bias_towards_adds_should_be_present_in_merged():
    # Arrange.
    first_replica = LwwElementGraph(bias=Bias.ADDS)
    second_replica = LwwElementGraph(bias=Bias.ADDS)

    with freeze_time() as frozen_time:
        # Element was present only in first.
        first_replica.add_vertex("1")

        # Time moves.
        frozen_time.tick()

        # At the same moment,
        # element was removed from first and added to second.
        first_replica.remove_vertex("1")
        second_replica.add_vertex("1")

    # Act.
    merged_replica = first_replica.merge(second_replica)

    # Assert.
    assert merged_replica.has_vertex("1") is True


def test_bias_towards_removes_should_not_be_present_in_merged():
    # Arrange.
    first_replica = LwwElementGraph(bias=Bias.REMOVES)
    second_replica = LwwElementGraph(bias=Bias.REMOVES)

    with freeze_time() as frozen_time:
        # Element was present only in first.
        first_replica.add_vertex("1")

        # Time moves.
        frozen_time.tick()

        # At the same moment,
        # element was removed from first and added to second.
        first_replica.remove_vertex("1")
        second_replica.add_vertex("1")

    # Act.
    merged_replica = first_replica.merge(second_replica)

    # Assert.
    assert merged_replica.has_vertex("1") is False


def test_later_add_timestamp_takes_precendence():
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


def test_later_remove_timestamp_takes_precendence():
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
