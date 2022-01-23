from lww_element_graph.structures.lww_element_graph import LwwElementGraph


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


def test_get_adjacent_vertexes():
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
    adjacent_vertexes = graph.get_adjacent_vertexes("1")

    # Assert.
    assert adjacent_vertexes == frozenset({"2", "3", "4"})
