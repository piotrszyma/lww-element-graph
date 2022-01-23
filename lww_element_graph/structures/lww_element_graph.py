from typing import Optional, TypeVar

from lww_element_graph.structures.lww_element_set import Bias, LwwElementSet

T = TypeVar("T")

VertexId = str

# Private structure representing edge.
# It should hold that len(_Edge) == 2
_Edge = frozenset[VertexId]


class LwwElementGraph:
    def __init__(
        self,
        initial_vertexes: LwwElementSet[VertexId] = None,
        initial_edges: LwwElementSet[_Edge] = None,
        bias = Bias.ADDS,
    ):
        self.vertexes = initial_vertexes or LwwElementSet(bias=bias)
        self.edges = initial_edges or LwwElementSet(bias=bias)

    def __repr__(self):
        return f"<LwwElementGraph {self.vertexes=} {self.edges=}>"

    def add_vertex(self, vertex_id: VertexId) -> None:
        """Adds vertex to the structure."""
        self.vertexes.add(vertex_id)

    def _has_any_edge_connected(self, vertex_id: VertexId) -> bool:
        return any((vertex_id in edge) for edge in self.edges.values())

    def remove_vertex(self, vertex_id: VertexId) -> None:
        """Removes vertex from the structure."""

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
        # TODO(szyma): Maybe add support for loops (edge connected to same vertex)?
        self.edges.add(self._build_edge(first_vertex_id, second_vertex_id))

    def remove_edge(
        self, first_vertex_id: VertexId, second_vertex_id: VertexId
    ) -> None:
        """Removes edge from the structure."""
        # TODO(szyma): Maybe add support for loops (edge connected to same vertex)?
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

    def merge(self, other: "LwwElementGraph") -> "LwwElementGraph":
        """Merges two graphs."""
        merged_vertexes = self.vertexes.merge(other.vertexes)
        merged_edges = self.edges.merge(other.edges)

        for edge in merged_edges.values():
            first_vertex_id, second_vertex_id = edge
            if (
                first_vertex_id not in merged_vertexes
                or second_vertex_id not in merged_vertexes
            ):
                merged_edges.remove(edge)

        return LwwElementGraph(
            initial_edges=merged_edges, initial_vertexes=merged_vertexes
        )
