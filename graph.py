import typing as tp
import random
import numpy as np
from vector import *
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, vertexes: tp.Iterable[tp.Any]):
        self.n = 0
        self.vertexes: list[tp.Any] = []
        self.matrix: list[list[int]] = []
        self.extend_vertex(vertexes)
        self.visited = [False] * self.n

    def is_connected(self, v: int, u: int):
        return u in self.matrix[v]

    def add_vertex(self, data: tp.Any):
        self.vertexes.append(data)
        self.matrix.append([])
        self.n += 1

    def extend_vertex(self, data: tp.Iterable[tp.Any]):
        for d in data:
            self.add_vertex(d)

    @staticmethod
    def arrange_data(*data: int):
        new_data = [x for x in data]
        new_data.sort()
        return new_data

    def make_connections(self, i: int, j: int):
        x, y = self.arrange_data(i, j)
        if y >= len(self.vertexes) or y >= len(self.vertexes) or x < 0 or y < 0:
            raise IndexError
        if not self.is_connected(x, y) and x != y:
            self.matrix[x].append(y)
            self.matrix[y].append(x)

    def bypass_graph(self):
        for i in range(self.n):
            if not self.visited[i]:
                self.dfs(i)
        self.visited = [False] * self.n

    def dfs(self, v: int):
        print(self.vertexes[v])
        self.visited[v] = True
        for u in self.matrix[v]:
            if not self.visited[u]:
                self.dfs(u)

    def __str__(self):
        return str(self.matrix)


class GraphNode:
    def __init__(self, pos: Vector2, data: tp.Any):
        self.pos = pos
        self.data = data


class GraphVisualization:
    def __init__(self, graph: Graph, min_distance: float = 1):
        self.graph = graph
        self.nodes: list[GraphNode] = []
        self.min_distance = min_distance

    def get_coordinates_rows(self) -> tuple[np.ndarray, np.ndarray]:
        x_data = []
        y_data = []
        for node in self.nodes:
            x_data.append(node.pos.x)
            y_data.append(node.pos.y)
        return np.array(x_data), np.array(y_data)

    def get_random_position(self):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        vec = Vector2(x, y)
        while not vec.is_no_near_points([pos.pos for pos in self.nodes], self.min_distance):
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            vec = Vector2(x, y)
        return vec

    def set_points_randomly(self):
        for vertex in self.graph.vertexes:
            vec = self.get_random_position()
            self.nodes.append(GraphNode(vec, vertex))

    def set_points(self):
        plt.plot(*self.get_coordinates_rows(), 'o')
        for i, line in enumerate(self.graph.matrix):
            for j, v in enumerate(line):
                x1 = self.nodes[i].pos.x
                y1 = self.nodes[i].pos.y
                x2 = self.nodes[v].pos.x
                y2 = self.nodes[v].pos.y
                plt.plot([x1, x2], [y1, y2])

    def show_graph(self):
        plt.show()

    def balanced_graph(self, step: float):
        for a in range(10000):
            for u, line in enumerate(self.graph.matrix):
                for j, v in enumerate(line):
                    pos = self.nodes[v].pos
                    if Vector2.distance(pos, self.nodes[u].pos) >= self.min_distance:
                        self.nodes[u].pos = self.nodes[u].pos.move_to(pos, step * Vector2.distance(self.nodes[u].pos, pos))
