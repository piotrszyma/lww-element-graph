# A state-based CRDT (CvRDT) must...

# Have a partial order to the values.
# "Monotonically increase" in state, meaning a new state only ever succeeds the current state in the value's ordering.
# Define a merge function ("least upper bound") which is idempotent and order-independent.
# TODO: Test partial ordering, monotonically increase.
# TODO: Implement compare fn?

from lww_element_graph.structures.lww_element_graph import LwwElementGraph


def test_merge_is_order_independent():
    # Arrange.
    first_replica: LwwElementGraph[int] = LwwElementGraph()
    second_replica: LwwElementGraph[int] = LwwElementGraph()

    first_replica.add_vertex("1")
    first_replica.add_vertex("2")
    first_replica.add_edge("1", "2")

    second_replica.add_vertex("1")
    second_replica.add_vertex("2")
    second_replica.add_edge("1", "2")

    first_replica.set_vertex_value("1", 456)
    second_replica.set_vertex_value("2", 123)

    # Act & Assert.
    assert first_replica.merge(second_replica) == second_replica.merge(first_replica)



def test_merge_is_idempotent():
    # Arrange.
    first_replica: LwwElementGraph[int] = LwwElementGraph()

    first_replica.add_vertex("1")
    first_replica.add_vertex("2")
    first_replica.add_edge("1", "2")

    # Act & Assert.
    assert first_replica.merge(first_replica) == first_replica




