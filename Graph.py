from asyncio import PriorityQueue
from Connection import Connection
from functools import reduce
from operator import add
from typing import Callable
import asyncio


class Graph:
    def __init__(self, conns: list[Connection]) -> None:
        self.edges: list[Connection] = conns
        self.vertices = list(
            [x.name for x in reduce(add, [list(i.get_nodes()) for i in conns])]
        )
        self.people = {(i.a.name, i.b.name): 0 for i in self.edges}
        self.num_v = len(self.vertices)

    def get_outward_edges(self, vertex: str) -> dict[str, Callable[[int], float]]:
        return {i.b.name: i.f for i in self.edges if i.a.name == vertex}

    def get_inward_edges(self, vertex: str) -> dict[str, Callable[[int], float]]:
        return {i.a.name: i.f for i in self.edges if i.b.name == vertex}

    async def dijkstra(self, start_vertex, end_vertex):
        D = {vertex: float("inf") for vertex in self.vertices}
        D[start_vertex] = 0
        visited = []

        pq = PriorityQueue()
        await pq.put((0, start_vertex))

        while not pq.empty():
            (dist, current_vertex) = await pq.get()
            visited.append(current_vertex)
            current_neighbors = self.get_outward_edges(current_vertex)

            for neighbor in current_neighbors.keys():
                func = self.get_outward_edges(current_vertex).get(neighbor)
                distance = func(self.people[(current_vertex, neighbor)] + 1)
                print(
                    f"distance between: {current_vertex} and {neighbor} is {distance}"
                )
                if neighbor not in visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_vertex] + distance
                    if new_cost < old_cost:
                        D[neighbor] = new_cost
                        await pq.put((new_cost, neighbor))

        path = []
        current_node = end_vertex
        print("Constructing path")
        while current_node != start_vertex:
            path.append(current_node)
            neighbors = self.get_inward_edges(current_node)
            min_distance = float("inf")
            next_node = None
            for neighbor in neighbors:
                func = self.get_outward_edges(neighbor).get(current_node)
                distance = func(self.people[(neighbor, current_node)] + 1)
                if D[neighbor] + distance < min_distance:
                    min_distance = D[neighbor] + distance
                    next_node = neighbor
            current_node = next_node
        path.append(start_vertex)
        path.reverse()

        return D[end_vertex], path

    def increase_people(self, path: list[str]):
        for i in range(len(path) - 1):
            self.people[(path[i], path[i + 1])] += 1

    def get_increase_amount(self, path: list[str]):
        res = 0
        for i in range(len(path) - 1):
            func = self.get_outward_edges(path[i]).get(path[i + 1])
            res += func(self.people[(path[i], path[i + 1])] + 1) - func(
                self.people[(path[i], path[i + 1])]
            )
        return res

    def decrease_people(self, path: list[str]):
        for i in range(len(path) - 1):
            self.people[(path[i], path[i + 1])] -= 1

    def get_path_length(self, path: list[str]):
        if path == []:
            return float("inf")
        res = 0
        for i in range(len(path) - 1):
            func = self.get_outward_edges(path[i]).get(path[i + 1])
            res += func(self.people[(path[i], path[i + 1])])
        return res

    async def find_path_for_population(
        self, start_vertex: str, end_vertex: str, population: int
    ):
        paths: list[list[str]] = [[] for i in range(population)]
        can_change = True

        while can_change:
            can_change = False
            for i in range(population):
                (path_len, path) = await self.dijkstra(start_vertex, end_vertex)
                print(
                    f"path: {path}, path_len: {path_len}, increase_amount: {self.get_increase_amount(path)} paths[i]: {paths[i]} old_path_len: {self.get_path_length(paths[i])}"
                )
                if path != paths[i] and path_len + self.get_increase_amount(
                    path
                ) < self.get_path_length(paths[i]):
                    can_change = True
                    self.increase_people(path)
                    self.decrease_people(paths[i])
                    paths[i] = path

        return paths, [self.get_path_length(i) for i in paths]
