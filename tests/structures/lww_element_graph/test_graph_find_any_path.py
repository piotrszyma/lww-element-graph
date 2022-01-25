from lww_element_graph.structures.lww_element_graph import LwwElementGraph


def test_path_between_same_vertex():
    # Arrange.
    graph = LwwElementGraph()
    graph.add_vertex("1")
    graph.add_vertex("2")
    graph.add_vertex("3")
    graph.add_vertex("4")
    graph.add_vertex("5")
    graph.add_vertex("6")
    graph.add_edge("1", "2")
    graph.add_edge("2", "3")
    graph.add_edge("3", "4")
    graph.add_edge("1", "6")

    # Act.
    path = graph.find_any_path("1", "1")

    # Assert.
    assert path == ("1",), "Path between same vertex should be that vertex only."


def test_path():
    # Arrange.
    graph = LwwElementGraph()
    graph.add_vertex("1")
    graph.add_vertex("2")
    graph.add_vertex("3")
    graph.add_vertex("4")
    graph.add_vertex("5")
    graph.add_vertex("6")
    graph.add_edge("1", "2")
    graph.add_edge("2", "3")
    graph.add_edge("3", "4")
    graph.add_edge("1", "6")

    # Act.
    path = graph.find_any_path("1", "4")

    # Assert.
    assert path == ("1", "2", "3", "4"), "Path between vertexes should be found."


def test_path_graph_with_cycle():
    """Tests if no infinite loop occurs when searching for path."""
    # Arrange.
    graph = LwwElementGraph()
    graph.add_vertex("1")
    graph.add_vertex("2")
    graph.add_vertex("3")
    graph.add_vertex("4")
    graph.add_vertex("5")
    graph.add_vertex("6")
    graph.add_edge("1", "2")
    graph.add_edge("2", "3")
    graph.add_edge("3", "4")
    graph.add_edge("2", "6")
    graph.add_edge("5", "6")
    graph.add_edge("5", "4")

    # Act.
    path = graph.find_any_path("1", "4")

    # Assert.
    assert path is not None, "Path between vertexes should be found."


def test_no_path():
    # Arrange.
    graph = LwwElementGraph()
    graph.add_vertex("1")
    graph.add_vertex("2")
    graph.add_vertex("3")
    graph.add_vertex("4")
    graph.add_vertex("5")
    graph.add_vertex("6")
    graph.add_edge("1", "2")
    graph.add_edge("3", "4")
    graph.add_edge("1", "6")

    # Act.
    path = graph.find_any_path("1", "4")

    # Assert.
    assert path is None, "Path should not be found."
