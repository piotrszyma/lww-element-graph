"""This module contains implementation of a LWW-Element-Graph.

A Graph that stores edges and vertices in a LwwElementSet,
implements merge operation- is a CRDT.
"""
from typing import Generic, Optional, TypeVar

from lww_element_graph.structures.lww_element_set import Bias, LwwElementSet
from lww_element_graph.types import SupportsRichComparison


T = TypeVar("T", bound=SupportsRichComparison)

VertexId = str

# Private structure representing edge.
# It should hold that len(_Edge) == 2
_Edge = frozenset[VertexId]


class GraphOperationError(Exception):
    pass


class LwwElementGraph(Generic[T]):
    def __init__(
        self,
        bias=Bias.ADDS,
        _initial_vertices: LwwElementSet[VertexId] = None,
        _initial_edges: LwwElementSet[_Edge] = None,
        _initial_vertices_values: dict[VertexId, T] = None,
    ):
        self.vertices = _initial_vertices or LwwElementSet(bias=bias)
        self.vertices_values: dict[VertexId, T] = _initial_vertices_values or {}

        self.edges = _initial_edges or LwwElementSet(bias=bias)

    def __repr__(self):
        return f"<LwwElementGraph {self.vertices=} {self.edges=}>"

    def __eq__(self, other: "LwwElementGraph[T]") -> bool:
        return (
            frozenset(self.vertices.values()) == frozenset(other.vertices.values())
            and frozenset(self.edges.values()) == frozenset(other.edges.values())
            and self.vertices_values == other.vertices_values
        )

    def add_vertex(self, vertex_id: VertexId) -> None:
        """Adds vertex to the graph."""
        if self.has_vertex(vertex_id):
            raise GraphOperationError(f"Vertex with id {vertex_id} already in graph.")
        self.vertices.add(vertex_id)

    def _assert_vertex_in_graph(self, vertex_id: VertexId) -> None:
        """Raises GraphOperationError if vertex not found in graph."""
        if not self.has_vertex(vertex_id):
            raise GraphOperationError(f"{vertex_id=} not found in graph")

    def set_vertex_value(self, vertex_id: VertexId, value: T) -> None:
        """Updates value associated with a vertex."""
        self._assert_vertex_in_graph(vertex_id)
        self.vertices.add(vertex_id)  # Simulate add - it will update timestamp.
        self.vertices_values[vertex_id] = value

    def get_vertex_value(self, vertex_id: VertexId) -> Optional[T]:
        """Returns value associated with a vertex, None if no value associated."""
        self._assert_vertex_in_graph(vertex_id)
        return self.vertices_values.get(vertex_id)

    def _has_any_edge_connected(self, vertex_id: VertexId) -> bool:
        self._assert_vertex_in_graph(vertex_id)
        return any((vertex_id in edge) for edge in self.edges.values())

    def remove_vertex(self, vertex_id: VertexId) -> None:
        """Removes vertex from the structure."""
        self._assert_vertex_in_graph(vertex_id)

        if self._has_any_edge_connected(vertex_id):
            raise GraphOperationError("Cannot remove vertex if it has edges connected.")

        self.vertices.remove(vertex_id)

    def has_vertex(self, vertex_id: VertexId) -> bool:
        """Returns boolean indicating if vertex is in structure."""
        return vertex_id in self.vertices

    def _build_edge(
        self, first_vertex_id: VertexId, second_vertex_id: VertexId
    ) -> frozenset[VertexId]:
        """Builds an edge - a frozenset with ids of two vertices."""
        if first_vertex_id == second_vertex_id:
            raise GraphOperationError("Graph does not support loops.")
        return frozenset((first_vertex_id, second_vertex_id))

    def add_edge(self, first_vertex_id: VertexId, second_vertex_id: VertexId) -> None:
        """Adds edge to the structure."""
        edge = self._build_edge(first_vertex_id, second_vertex_id)
        if edge in self.edges:
            raise GraphOperationError(f"Edge {edge} already in graph.")
        self.edges.add(edge)

    def remove_edge(
        self, first_vertex_id: VertexId, second_vertex_id: VertexId
    ) -> None:
        """Removes edge from the structure."""
        edge = self._build_edge(first_vertex_id, second_vertex_id)
        if edge not in self.edges:
            raise GraphOperationError(f"Edge {edge} not found in graph.")
        self.edges.remove(edge)

    def has_edge(self, first_vertex_id: VertexId, second_vertex_id: VertexId) -> bool:
        """Returns boolean indicating if graph has edge connecting vertices."""
        return frozenset({first_vertex_id, second_vertex_id}) in self.edges

    def get_adjacent_vertices(self, vertex_id: VertexId) -> frozenset[VertexId]:
        """Returns a frozenset of vertices adjacent to the vertex."""
        self._assert_vertex_in_graph(vertex_id)

        adjacent_vertices = []
        for edge in self.edges.values():
            assert len(edge) == 2, "Edges should be of length 2."

            if vertex_id not in edge:
                continue

            (adjacent_vertex_id,) = edge - {vertex_id}
            adjacent_vertices.append(adjacent_vertex_id)
        return frozenset(adjacent_vertices)

    def find_any_path(
        self, first_vertex_id: VertexId, second_vertex_id: VertexId
    ) -> Optional[tuple[VertexId, ...]]:
        """Finds a path between two vertices using BFS."""
        self._assert_vertex_in_graph(first_vertex_id)
        self._assert_vertex_in_graph(second_vertex_id)

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

            for adjacent_vertex in self.get_adjacent_vertices(current_vertex):
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

    def _merge_vertices_values(
        self, other: "LwwElementGraph", merged_vertices: LwwElementSet[VertexId]
    ) -> dict[VertexId, T]:
        self_values = self.vertices_values
        other_values = other.vertices_values
        merged_values: dict[VertexId, T] = {}

        for vertex_id in merged_vertices.values():
            if vertex_id in self_values and vertex_id in other_values:
                timestamp = merged_vertices.add_timestamps[vertex_id]
                self_timestamp = self.vertices.add_timestamps[vertex_id]
                other_timestamp = other.vertices.add_timestamps[vertex_id]
                if timestamp == self_timestamp == other_timestamp:
                    # Edge case: different replicas assigned different value
                    # in the exact same moment - take max of those two values.
                    merged_values[vertex_id] = max(
                        self.vertices_values[vertex_id],
                        other.vertices_values[vertex_id],
                    )
                elif timestamp == self_timestamp:
                    merged_values[vertex_id] = self.vertices_values[vertex_id]
                else:
                    merged_values[vertex_id] = other.vertices_values[vertex_id]
            elif vertex_id in self_values:
                merged_values[vertex_id] = self.vertices_values[vertex_id]
            elif vertex_id in other_values:
                merged_values[vertex_id] = other.vertices_values[vertex_id]

        return merged_values

    def _remove_orphant_edges(
        self,
        merged_edges: LwwElementSet[_Edge],
        merged_vertices: LwwElementSet[VertexId],
    ) -> None:
        for edge in merged_edges.values():
            first_vertex_id, second_vertex_id = edge
            if (
                first_vertex_id not in merged_vertices
                or second_vertex_id not in merged_vertices
            ):
                merged_edges.remove(edge)

    def _assertbias_equals(self, other: "LwwElementGraph") -> None:
        expectedbias = self.vertices.bias
        vertices_samebias = self.vertices.bias == other.vertices.bias == expectedbias
        edges_samebias = self.edges.bias == other.edges.bias == expectedbias
        if not vertices_samebias or not edges_samebias:
            raise GraphOperationError("Each Graph should have same bias.")

    def merge(self, other: "LwwElementGraph") -> "LwwElementGraph":
        """Merges two graphs.

        It performs the merge with the following steps:

        1. merges vertices & edges using LwwElementSet.
        2. merges vertices values given verties timestamps from merged LwwElementSet
        3. removes edges which connect vertices removed during merge
        """
        self._assertbias_equals(other)

        merged_vertices = self.vertices.merge(other.vertices)
        merged_edges = self.edges.merge(other.edges)

        merged_values: dict[VertexId, T] = self._merge_vertices_values(
            other, merged_vertices
        )
        self._remove_orphant_edges(merged_edges, merged_vertices)

        return LwwElementGraph(
            _initial_edges=merged_edges,
            _initial_vertices=merged_vertices,
            _initial_vertices_values=merged_values,
        )
