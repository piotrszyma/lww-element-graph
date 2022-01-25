# LWWElementGraph

An implementation of a last write wins, state-based conflict-free replicated data graph.

1. Graph is undirected
1. Graph does not support multiple edges connecting same vertices
1. Graph does not support loops
1. Graph does not support assigning values to edges
1. Graph does support assigning values to vertices

## Usage example

```python
from lww_element_graph.structures.lww_element_graph import LwwElementGraph

first_replica = LwwElementGraph()
first_replica.add_vertex("1")  # Add vertex.
first_replica.add_vertex("2")
first_replica.add_edge("1", "2")  # Connect vertices with edge.
first_replica.set_vertex_value("1", "foo")  # Assign a value to a vertex.

second_replica = LwwElementGraph()
second_replica.add_vertex("3")  # Add vertex.

merged_replica = first_replica.merge(second_replica)  # Merge two replicas.

```

For more usage examples, please check `tests/` directory.

## Installation

```
poetry install
```

## Run tests

```
poetry run pytest
```

## Run coverage
```
poetry run pytest --cov=lww_element_graph tests/
```

## Run coverage (html)
```
poetry run pytest --cov-report html --cov=lww_element_graph tests/
```
