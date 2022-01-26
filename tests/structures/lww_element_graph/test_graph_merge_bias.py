from freezegun import freeze_time

from lww_element_graph.structures.lww_element_graph import LwwElementGraph
from lww_element_graph.structures.lww_element_set import Bias


def test_bias_towards_adds_element_added_and_removed_should_be_present_in_merged():
    """Fails if element will be present in merged graph.

    Element simultaniously added/removed - present after
    merge in biased towards ADDS.
    """
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


def test_bias_towards_removes_element_added_and_removed_should_not_be_present_merged():
    """Fails if element will be present in merged graph.

    Element simultaniously added/removed - should not be present
    after merge in biased towards REMOVES.
    """
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
