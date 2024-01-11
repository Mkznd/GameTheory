from Node import Node
from typing import Callable


class Connection:
    def __init__(
        self, a: Node, b: Node, f: Callable[[int], float] = lambda _: 1
    ) -> None:
        self.a = a
        self.b = b
        self.f = f

    def get_nodes(self) -> (Node, Node):
        return self.a, self.b

    def __str__(self):
        return f"{self.a.name} {self.b.name}"

    def __repr__(self):
        return f"{self.a.name} {self.b.name}"
