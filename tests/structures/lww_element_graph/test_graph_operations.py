import pytest

from lww_element_graph.structures.lww_element_graph import (
    GraphOperationError,
    LwwElementGraph,
)


def test_insert_vertex():
    # Arrange.
    graph = LwwElementGraph()

    # Act.
    graph.add_vertex("1")

    # Assert.
    assert graph.has_vertex("1") is True


def test_insert_edge():
    # Arrange.
    graph = LwwElementGraph()
    graph.add_vertex("1")
    graph.add_vertex("2")

    # Act.
    graph.add_edge("1", "2")

    # Assert.
    assert graph.has_edge("1", "2") is True


def test_remove_vertex():
    # Arrange.
    graph = LwwElementGraph()
    graph.add_vertex("1")

    # Act.
    graph.remove_vertex("1")

    # Assert.
    assert graph.has_vertex("1") is False


def test_remove_edge():
    # Arrange.
    graph = LwwElementGraph()
    graph.add_vertex("1")
    graph.add_vertex("2")
    graph.add_edge("1", "2")

    # Act.
    graph.remove_edge("1", "2")

    # Assert.
    assert graph.has_edge("1", "2") is False


def test_check_vertex_is_in_graph():
    # Arrange.
    graph = LwwElementGraph()
    graph.add_vertex("1")

    # Act & assert.
    assert graph.has_vertex("1") is True


def test_check_edge_is_in_graph():
    # Arrange.
    graph = LwwElementGraph()
    graph.add_vertex("1")
    graph.add_vertex("2")
    graph.add_edge("1", "2")

    # Act & assert.
    assert graph.has_edge("1", "2") is True


def test_check_vertex_is_not_in_graph():
    # Arrange.
    graph = LwwElementGraph()

    # Act & assert.
    assert graph.has_vertex("1") is False


def test_check_edge_is_not_in_graph():
    # Arrange.
    graph = LwwElementGraph()

    # Act & assert.
    assert graph.has_edge("1", "2") is False


def test_get_adjacent_vertices():
    # Arrange.
    graph = LwwElementGraph()
    graph.add_vertex("1")
    graph.add_vertex("2")
    graph.add_vertex("3")
    graph.add_vertex("4")
    graph.add_vertex("5")
    graph.add_vertex("6")
    graph.add_edge("1", "2")
    graph.add_edge("1", "3")
    graph.add_edge("1", "4")
    graph.add_edge("2", "4")
    graph.add_edge("2", "6")

    # Act.
    adjacent_vertices = graph.get_adjacent_vertices("1")

    # Assert.
    assert adjacent_vertices == frozenset({"2", "3", "4"})


def test_add_same_vertex_twice_raises_error():
    # Arrange.
    graph = LwwElementGraph()
    graph.add_vertex("1")

    # Act & Assert.
    with pytest.raises(GraphOperationError, match="already in graph."):
        graph.add_vertex("1")


def test_remove_vertex_with_connected_edges_raises_error():
    graph = LwwElementGraph()
    graph.add_vertex("1")
    graph.add_vertex("2")
    graph.add_edge("1", "2")

    # Act & Assert.
    with pytest.raises(GraphOperationError, match="has edges connected."):
        graph.remove_vertex("1")


def test_remove_nonexistent_vertex_raises_error():
    graph = LwwElementGraph()

    # Act & Assert.
    with pytest.raises(GraphOperationError, match="not found in graph"):
        graph.remove_vertex("1")


def test_add_loop_raises_error():
    graph = LwwElementGraph()
    graph.add_vertex("1")

    # Act & Assert.
    with pytest.raises(GraphOperationError, match="does not support loops"):
        graph.add_edge("1", "1")


def test_remove_nonexistent_edge_raises_error():
    graph = LwwElementGraph()
    graph.add_vertex("1")
    graph.add_vertex("2")

    # Act & Assert.
    with pytest.raises(GraphOperationError, match="not found in graph"):
        graph.remove_edge("1", "2")


def test_add_existing_edge_raises_error():
    graph = LwwElementGraph()
    graph.add_vertex("1")
    graph.add_vertex("2")
    graph.add_edge("1", "2")

    # Act & Assert.
    with pytest.raises(GraphOperationError, match="already in graph"):
        graph.add_edge("1", "2")
