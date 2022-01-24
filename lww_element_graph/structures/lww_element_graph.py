from typing import Generic, Optional, TypeVar

from lww_element_graph.structures.lww_element_set import Bias, LwwElementSet

T = TypeVar("T")

VertexId = str

# Private structure representing edge.
# It should hold that len(_Edge) == 2
_Edge = frozenset[VertexId]


class LwwElementGraph(Generic[T]):
    def __init__(
        self,
        initial_vertexes: LwwElementSet[VertexId] = None,
        initial_edges: LwwElementSet[_Edge] = None,
        initial_vertexes_values: dict[VertexId, T] = None,
        bias=Bias.ADDS,
    ):
        self.vertexes = initial_vertexes or LwwElementSet(bias=bias)
        self.vertexes_values: dict[VertexId, T] = initial_vertexes_values or {}

        self.edges = initial_edges or LwwElementSet(bias=bias)

    def __repr__(self):
        return f"<LwwElementGraph {self.vertexes=} {self.edges=}>"

    def add_vertex(self, vertex_id: VertexId) -> None:
        """Adds vertex to the graph."""
        self.vertexes.add(vertex_id)

    def _assert_vertex_in_graph(self, vertex_id: VertexId) -> None:
        """Raises ValueError if vertex not found in graph."""
        if not self.has_vertex(vertex_id):
            raise ValueError(f"{vertex_id=} not found in graph")

    def set_vertex_value(self, vertex_id, value: T) -> None:
        """Updates value associated with a vertex."""
        self._assert_vertex_in_graph(vertex_id)
        self.vertexes_values[vertex_id] = value

    def get_vertex_value(self, vertex_id: VertexId) -> Optional[T]:
        """Returns value associated with a vertex, None if no value associated."""
        self._assert_vertex_in_graph(vertex_id)
        return self.vertexes_values.get(vertex_id)

    def _has_any_edge_connected(self, vertex_id: VertexId) -> bool:
        return any((vertex_id in edge) for edge in self.edges.values())

    def remove_vertex(self, vertex_id: VertexId) -> None:
        """Removes vertex from the structure."""
        self._assert_vertex_in_graph(vertex_id)

        if self._has_any_edge_connected(vertex_id):
            raise ValueError("Cannot remove vertex if it has edges connected.")

        self.vertexes.remove(vertex_id)

    def has_vertex(self, vertex_id: VertexId) -> bool:
        """Returns boolean indicating if vertex is in structure."""
        return vertex_id in self.vertexes

    def _build_edge(
        self, first_vertex_id: VertexId, second_vertex_id: VertexId
    ) -> frozenset[VertexId]:
        """Builds an edge - a frozenset with ids of two vertexes."""
        assert (
            first_vertex_id != second_vertex_id
        ), "Loops are not supported by this graph."
        return frozenset((first_vertex_id, second_vertex_id))

    def add_edge(self, first_vertex_id: VertexId, second_vertex_id: VertexId) -> None:
        """Adds edge to the structure."""
        self.edges.add(self._build_edge(first_vertex_id, second_vertex_id))

    def remove_edge(
        self, first_vertex_id: VertexId, second_vertex_id: VertexId
    ) -> None:
        """Removes edge from the structure."""
        self.edges.remove(self._build_edge(first_vertex_id, second_vertex_id))

    def has_edge(self, first_vertex_id: VertexId, second_vertex_id: VertexId) -> bool:
        """Returns boolean indicating if graph has edge connecting vertexes."""
        return frozenset({first_vertex_id, second_vertex_id}) in self.edges

    def get_adjacent_vertexes(self, vertex_id: VertexId) -> frozenset[VertexId]:
        """Returns a frozenset of vertexes adjacent to the vertex."""
        adjacent_vertexes = []
        for edge in self.edges.values():
            assert len(edge) == 2, "Edges should be of length 2."

            if vertex_id not in edge:
                continue

            (adjacent_vertex_id,) = edge - {vertex_id}
            adjacent_vertexes.append(adjacent_vertex_id)
        return frozenset(adjacent_vertexes)

    def find_any_path(
        self, first_vertex_id: VertexId, second_vertex_id: VertexId
    ) -> Optional[tuple[VertexId, ...]]:
        """Finds a path between two vertexes using BFS."""
        if first_vertex_id == second_vertex_id:
            return (first_vertex_id,)

        visited: set[VertexId] = set()
        paths_from_first: dict[VertexId, tuple[VertexId, ...]] = {
            first_vertex_id: (first_vertex_id,)
        }

        to_visit = [first_vertex_id]

        while to_visit:
            current_vertex = to_visit.pop()

            # Mark current vertex as visited.
            visited.add(current_vertex)

            for adjacent_vertex in self.get_adjacent_vertexes(current_vertex):
                if adjacent_vertex in visited:
                    # Skip adjacent that is already visited.
                    continue

                if adjacent_vertex == second_vertex_id:
                    # If the adjacent vertex is target vertex, we found the path.
                    return (*paths_from_first[current_vertex], adjacent_vertex)

                paths_from_first[adjacent_vertex] = (
                    *paths_from_first[current_vertex],
                    adjacent_vertex,
                )
                to_visit.append(adjacent_vertex)

        return None

    def _merge_vertexes_values(
        self, merged_vertexes: LwwElementSet[VertexId], other: "LwwElementGraph"
    ) -> dict[VertexId, T]:
        self_values = self.vertexes_values
        other_values = other.vertexes_values
        merged_values: dict[VertexId, T] = {}

        for vertex_id in merged_vertexes.values():
            if vertex_id in self_values and vertex_id in other_values:
                timestamp = merged_vertexes.add_timestamps[vertex_id]
                if timestamp == self.vertexes.add_timestamps[vertex_id]:
                    merged_values[vertex_id] = self.vertexes_values[vertex_id]
                else:
                    merged_values[vertex_id] = other.vertexes_values[vertex_id]
            elif vertex_id in self_values:
                merged_values[vertex_id] = self.vertexes_values[vertex_id]
            elif vertex_id in other_values:
                merged_values[vertex_id] = other.vertexes_values[vertex_id]

        return merged_values

    def _remove_orphant_edges(
        self,
        merged_edges: LwwElementSet[_Edge],
        merged_vertexes: LwwElementSet[VertexId],
    ) -> None:
        for edge in merged_edges.values():
            first_vertex_id, second_vertex_id = edge
            if (
                first_vertex_id not in merged_vertexes
                or second_vertex_id not in merged_vertexes
            ):
                merged_edges.remove(edge)

    def merge(self, other: "LwwElementGraph") -> "LwwElementGraph":
        """Merges two graphs."""
        merged_vertexes = self.vertexes.merge(other.vertexes)
        merged_edges = self.edges.merge(other.edges)

        merged_values: dict[VertexId, T] = self._merge_vertexes_values(
            merged_vertexes, other
        )
        self._remove_orphant_edges(merged_edges, merged_vertexes)

        return LwwElementGraph(
            initial_edges=merged_edges,
            initial_vertexes=merged_vertexes,
            initial_vertexes_values=merged_values,
        )
