"""
Fill the slots of a curriculum with courses, making sure that there is no overlap
within a block and respecting exclusivity rules.
"""

from typing import Optional

from ...course import ConcreteId, EquivalenceId, PseudoCourse

from ...courseinfo import CourseInfo
from .tree import CourseRecommendation, Leaf, Curriculum, Block
from dataclasses import dataclass, field


# Print debug messages when solving a curriculum.
DEBUG_SOLVE = False


@dataclass
class RecommendedCourse:
    # The original `CourseRecommendation` that spawned this course.
    rec: CourseRecommendation
    # The repetition index.
    # The recommendation repeat indices start after the taken indices.
    repeat_index: int


@dataclass
class TakenCourse:
    # The courseid of the course.
    course: PseudoCourse
    # The amount of credits of the course.
    # Must correspond to `course`.
    credits: int
    # The semester in which this course was taken.
    sem: int
    # Where in the semester was this course taken.
    index: int
    # Flattened index indicating where along the plan this course was taken.
    flat_index: int
    # `0` if this course is unique (by code) in the plan.
    # Otherwise, increments by one per every repetition.
    repeat_index: int


@dataclass
class TakenCourses:
    flat: list[TakenCourse]
    mapped: dict[str, list[TakenCourse]]


@dataclass
class Edge:
    cap: int
    flow: int
    src: int
    dst: int
    rev: int
    cost: int = 0


@dataclass
class Node:
    # Either:
    # - A curriculum `Block`
    # - A course, with a layer id `str` and course information.
    #   This course may be either taken by the student or recommended.
    # - No origin (eg. the virtual sink node)
    origin: Block | tuple[str, TakenCourse | RecommendedCourse] | None = None
    outgoing: list[Edge] = field(default_factory=list)
    incoming: list[Edge] = field(default_factory=list)

    def flow(self) -> int:
        f = 0
        for edge in self.outgoing:
            if edge.flow >= 0:
                f += edge.flow
        return f

    def cap(self) -> int:
        c = 0
        for edge in self.outgoing:
            c += edge.cap
        return c


@dataclass
class LayerCourses:
    """
    Stores the current course -> node id mappings.
    """

    # Contains an entry for each course code.
    # The nested dictionary maps from repeat indices to vertex ids.
    courses: dict[str, dict[int, int]]


class SolvedCurriculum:
    # List of nodes.
    # The ID of each node is its index in this list.
    nodes: list[Node]
    # Flat list of edges.
    edges: list[Edge]
    # The id of the universal source
    source: int
    # The id of the universal sink
    sink: int
    # The root curriculum.
    root: int
    # A dictionary from layer ids to a (list of node ids for each course).
    layers: dict[str, LayerCourses]

    def __init__(self):
        self.nodes = [Node(), Node()]
        self.edges = []
        self.source = 0
        self.sink = 1
        self.root = 1
        self.layers = {}

    def add(self, node: Node) -> int:
        id = len(self.nodes)
        self.nodes.append(node)
        return id

    def connect(self, src_id: int, dst_id: int, cap: int, cost: int = 0):
        src = self.nodes[src_id]
        dst = self.nodes[dst_id]
        edge_fw = Edge(
            cap=cap, flow=0, src=src_id, dst=dst_id, rev=len(dst.outgoing), cost=cost
        )
        edge_rev = Edge(
            cap=0, flow=0, src=dst_id, dst=src_id, rev=len(src.outgoing), cost=-cost
        )
        src.outgoing.append(edge_fw)
        dst.incoming.append(edge_fw)
        dst.outgoing.append(edge_rev)
        src.incoming.append(edge_rev)
        self.edges.append(edge_fw)
        self.edges.append(edge_rev)

    def add_course(
        self,
        layer_id: str,
        code: str,
        repeat_index: int,
        credits: int,
        origin: TakenCourse | RecommendedCourse,
    ) -> int:
        layer = self.layers.setdefault(layer_id, LayerCourses(courses={}))
        ids = layer.courses.setdefault(code, {})
        if repeat_index in ids:
            return ids[repeat_index]
        id = self.add(Node(origin=(layer_id, origin)))
        ids[repeat_index] = id
        self.connect(self.source, id, credits)
        return id

    def dump_graphviz(self, taken: list[list[PseudoCourse]]) -> str:  # noqa: C901
        """
        Dump the graph representation as a Graphviz DOT file.
        """
        out = "digraph {\n"
        for id, node in enumerate(self.nodes):
            if id == self.source or id == self.sink:
                continue
            elif id == self.root:
                label = "Root"
            elif isinstance(node.origin, Block):
                label = f"{node.origin.name or f'b{id}'}"
                if isinstance(node.origin, Leaf) and node.origin.fill_with:
                    label += f"\n({len(node.origin.fill_with)} recommendations)"
            elif isinstance(node.origin, tuple):
                layer, c = node.origin
                if isinstance(c, TakenCourse):
                    label = c.course.code
                else:
                    label = f"[{c.rec.course.code}]"
                if layer != "":
                    label = f"{label}({layer})"
            else:
                label = f"v{id}"
            fountain = 0
            for edge in node.outgoing:
                if edge.dst == self.sink:
                    fountain -= edge.cap
            for edge in node.incoming:
                if edge.src == self.source:
                    fountain += edge.cap
            if fountain > 0:
                label += f" +{fountain}"
            elif fountain < 0:
                label += f" {fountain}"
            out += f'  v{id} [label="{label}"];\n'
        for edge in self.edges:
            if edge.cap == 0 or edge.src == self.source or edge.dst == self.sink:
                continue
            attrs = f'label="{edge.flow}/{edge.cap}"'
            if edge.flow == 0:
                attrs += " style=dotted"
            out += f"  v{edge.src} -> v{edge.dst} [{attrs}];\n"
        out += "}"
        return out


def _connect_course(
    courseinfo: CourseInfo,
    g: SolvedCurriculum,
    block: Leaf,
    superid: int,
    origin: TakenCourse | RecommendedCourse,
):
    """
    Create or look up the node corresponding to course `c` and connect it to the node
    `superid`.
    The caller must uphold that `superid` identifies the node corresponding to block
    `block`, and that the code of `c` is in `block.codes`.
    If the course `c` is repeated and the multiplicity of `block` does not allow it,
    the course is not connected.
    """
    if isinstance(origin, TakenCourse):
        course = origin.course
    else:
        course = origin.rec.course
    repeat_index = origin.repeat_index
    credits = courseinfo.get_credits(course)
    if credits is None:
        return
    elif credits == 0:
        credits = 1
    max_multiplicity = block.codes[course.code]
    if max_multiplicity is not None and repeat_index >= max_multiplicity:
        # Cannot connect to more than `max_multiplicity` courses at once
        return
    subid = g.add_course(block.layer, course.code, repeat_index, credits, origin)
    cost = 2
    if (
        isinstance(course, ConcreteId)
        and course.equivalence is not None
        and course.equivalence.code in block.codes
    ) or isinstance(course, EquivalenceId):
        # Prefer equivalence edges over non-equivalence edges
        # This makes sure that equivalences always count towards their corresponding
        # blocks if there is the option
        cost = 1
    if isinstance(origin, RecommendedCourse):
        cost = 1000 + origin.rec.cost
    g.connect(subid, superid, credits, cost)


def _build_visit(
    courseinfo: CourseInfo, g: SolvedCurriculum, taken: TakenCourses, block: Block
) -> int:
    superid = g.add(Node(origin=block))
    if isinstance(block, Leaf):
        # A list of courses
        # TODO: Prioritize edges just like SIDING

        # For performance, iterate through the taken courses or through the accepted
        # codes, whichever is shorter
        if len(block.codes) < len(taken.flat):
            # There is a small amount of courses in this block
            # Iterate through this list, in taken order
            minitaken: list[TakenCourse] = []
            for code in block.codes:
                if code in taken.mapped:
                    minitaken.extend(taken.mapped[code])
            minitaken.sort(key=lambda c: c.flat_index)
            for c in minitaken:
                _connect_course(courseinfo, g, block, superid, c)
        else:
            # There are way too many codes in this block
            # Iterate through taken courses instead
            for c in taken.flat:
                if c.course.code in block.codes:
                    _connect_course(courseinfo, g, block, superid, c)

        # Iterate over the recommended courses for this block
        recommend_index: dict[str, int] = {}
        for rec in block.fill_with:
            code = rec.course.code
            if code not in recommend_index:
                recommend_index[code] = (
                    len(taken.mapped[code]) if code in taken.mapped else 0
                )
            repeat_index = recommend_index[code]
            recommended = RecommendedCourse(rec=rec, repeat_index=repeat_index)
            _connect_course(courseinfo, g, block, superid, recommended)
            recommend_index[code] += 1
    else:
        # A combination of blocks
        for c in block.children:
            subid = _build_visit(courseinfo, g, taken, c)
            g.connect(subid, superid, c.cap)
    return superid


def _build_graph(
    courseinfo: CourseInfo,
    curriculum: Curriculum,
    taken_semesters: list[list[PseudoCourse]],
) -> SolvedCurriculum:
    """
    Take a curriculum prototype and a specific set of taken courses, and build a
    solvable graph that represents this curriculum.
    """

    taken = TakenCourses(flat=[], mapped={})
    for sem_i, sem in enumerate(taken_semesters):
        for i, c in sorted(enumerate(sem)):
            creds = courseinfo.get_credits(c)
            if creds is None:
                continue
            if creds == 0:
                # Assign 1 ghost credit to 0-credit courses
                # Kind of a hack, but works pretty well
                # The curriculum definition must correspondingly also consider
                # 0-credit courses to have 1 ghost credit
                creds = 1
            repetitions = taken.mapped.setdefault(c.code, [])
            c = TakenCourse(
                course=c,
                credits=creds,
                sem=sem_i,
                index=i,
                flat_index=len(taken.flat),
                repeat_index=len(repetitions),
            )
            repetitions.append(c)
            taken.flat.append(c)

    g = SolvedCurriculum()
    g.root = _build_visit(courseinfo, g, taken, curriculum.root)
    g.connect(g.root, g.sink, curriculum.root.cap)
    return g


INFINITY: int = 10**18


def _compute_shortest_path(
    g: SolvedCurriculum, src: int, dst: int
) -> Optional[list[Edge]]:
    # Bellman-Ford
    n = len(g.nodes)
    costs = [INFINITY for _i in range(n)]
    costs[src] = 0
    parent: list[Optional[Edge]] = [None for _i in range(n)]
    for _stage in range(n - 1):
        stop = True
        for edge in g.edges:
            if edge.flow < edge.cap and costs[edge.src] < INFINITY:
                new_cost = costs[edge.src] + edge.cost
                if new_cost < costs[edge.dst]:
                    costs[edge.dst] = new_cost
                    parent[edge.dst] = edge
                    stop = False
        if stop:
            break

    # Extract path (in reversed order, but who cares)
    if costs[dst] >= INFINITY:
        return None
    path: list[Edge] = []
    cur = dst
    while True:
        edge = parent[cur]
        if edge is None:
            break
        path.append(edge)
        cur = edge.src
    return path


def _max_flow_min_cost(g: SolvedCurriculum):
    # Iteratively improve flow
    while True:
        # Find shortest path from source to sink
        path = _compute_shortest_path(g, g.source, g.sink)
        if path is None:
            break

        # Find the maximum flow that can go through the path
        flow = INFINITY
        for edge in path:
            s = edge.cap - edge.flow
            if s < flow:
                flow = s

        # Apply flow to path
        for edge in path:
            edge.flow += flow
            g.nodes[edge.dst].outgoing[edge.rev].flow -= flow


def solve_curriculum(
    courseinfo: CourseInfo, curriculum: Curriculum, taken: list[list[PseudoCourse]]
) -> SolvedCurriculum:
    # Take the curriculum blueprint, and produce a graph for this student
    g = _build_graph(courseinfo, curriculum, taken)
    # Solve the flow problem on the produced graph
    _max_flow_min_cost(g)
    # Ensure that demand is satisfied
    # Recommended courses should always fill in missing demand
    # It's a bug if they cannot fill in the demand
    if g.nodes[g.root].flow() < g.nodes[g.root].cap():
        raise Exception(
            "maximizing flow does not satisfy the root demand,"
            + " even with filler recommendations"
            + f":\n{g.dump_graphviz(taken)}"
        )
    # Make sure that there is no split flow (ie. there is no course that splits its
    # outgoing flow between two blocks)
    # TODO: Do something about this edge case
    #   Solving this problem is NP-complete, but it is such an edge case that we can
    #   probably get away by trying all possible paths the split flow could take.
    for i, node in enumerate(g.nodes):
        if i == g.source:
            continue
        nonzero = 0
        for edge in node.outgoing:
            if edge.flow > 0:
                nonzero += 1
        if nonzero > 1:
            raise Exception(
                "min cost max flow produced invalid split-flow"
                + " (ie. there is some node with 2+ non-zero-flow outgoing edges)"
                + f":\n{g.dump_graphviz(taken)}"
            )
    return g
