from typing import TypeVar

from lww_element_graph.structures.lww_element_set import LwwElementSet

T = TypeVar("T")

VertexId = str

# Private structure representing edge.
# It should hold that len(_Edge) == 2
_Edge = frozenset[VertexId]


class LwwElementGraph:
    def __init__(self):
        self._vertexes: LwwElementSet[VertexId] = LwwElementSet()
        self._edges: LwwElementSet[_Edge] = LwwElementSet()

    def add_vertex(self, vertex_id: VertexId) -> None:
        """Adds vertex to the structure."""
        self._vertexes.add(vertex_id)

    def has_vertex(self, vertex_id: VertexId) -> bool:
        """Returns boolean indicating if vertex is in structure."""
        return vertex_id in self._vertexes

    def _build_edge(
        self, first_vertex_id: VertexId, second_vertex_id: VertexId
    ) -> frozenset[VertexId]:
        """Builds an edge - a frozenset with ids of two vertexes."""
        return frozenset((first_vertex_id, second_vertex_id))

    def add_edge(self, first_vertex_id: VertexId, second_vertex_id: VertexId) -> None:
        """Adds edge to the structure."""
        self._edges.add(self._build_edge(first_vertex_id, second_vertex_id))

    def get_adjacent_vertexes(self, vertex_id: VertexId) -> frozenset[VertexId]:
        """Returns a frozenset of vertexes adjacent to the vertex."""
        adjacent_vertexes = []
        for edge in self._edges.values():
            assert len(edge) == 2, "Edges should be of length 2."

            if vertex_id not in edge:
                continue

            (adjacent_vertex_id,) = edge - {vertex_id}
            adjacent_vertexes.append(adjacent_vertex_id)
        return frozenset(adjacent_vertexes)

    def find_any_path(
        self, first_vertex_id: VertexId, second_vertex_id: VertexId
    ) -> tuple[VertexId]:
        """Returns a path between two vertexes."""
        # TODO: Implement path finding - BFS from two vertexes.
        return tuple()
