from lww_element_graph.structures.lww_element_graph import LwwElementGraph


def test_merge_is_commutative():
    """Fails if merge operation is not commutative.

    Commutativity holds for operation MERGE when given elements A, B:
    A MERGE B = B MERGE A
    """
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

    # Act & assert.
    assert first_replica.merge(second_replica) == second_replica.merge(first_replica)


def test_merge_is_idempotent():
    """Fails if merge operation is not idempotent.

    Idempotence holds for operation MERGE when given element A:
    (A MERGE A) = A
    """
    # Arrange.
    first_replica: LwwElementGraph[int] = LwwElementGraph()

    first_replica.add_vertex("1")
    first_replica.add_vertex("2")
    first_replica.add_edge("1", "2")

    # Act & assert.
    assert first_replica.merge(first_replica) == first_replica


def test_merge_is_associative():
    """Fails if merge operation is not associative.

    Associativity holds for operation MERGE when given elements A, B, C:
    (A MERGE B) MERGE C = A MERGE (B MERGE C)
    """
    # Arrange.
    first_replica: LwwElementGraph[int] = LwwElementGraph()
    first_replica.add_vertex("1")
    first_replica.add_vertex("2")
    first_replica.add_edge("1", "2")

    second_replica: LwwElementGraph[int] = LwwElementGraph()
    second_replica.add_vertex("1")
    second_replica.add_vertex("3")
    second_replica.add_edge("1", "3")

    third_replica: LwwElementGraph[int] = LwwElementGraph()
    third_replica.add_vertex("2")
    third_replica.add_vertex("4")
    third_replica.add_edge("2", "4")

    # Act.
    first_result = first_replica.merge(second_replica).merge(third_replica)
    second_result = first_replica.merge(second_replica.merge(third_replica))

    # Assert.
    assert first_result == second_result
