from Connection import Connection
from Graph import Graph
from Node import Node
import asyncio


def main():
    conns = [
        Connection(Node("a"), Node("b"), lambda x: x),
        Connection(Node("a"), Node("c"), lambda x: 1),
        Connection(Node("b"), Node("e"), lambda x: 1),
        Connection(Node("c"), Node("e"), lambda x: x),
        Connection(Node("b"), Node("c"), lambda x: 0),
        Connection(Node("c"), Node("b"), lambda x: 0),
    ]
    g = Graph(conns)
    (paths, lens) = asyncio.run(g.find_path_for_population("a", "e", 5))
    print(paths, sum(lens) / len(lens))
    g.visualize()


if __name__ == "__main__":
    main()
