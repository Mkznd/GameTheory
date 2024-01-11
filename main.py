from Connection import Connection
from Graph import Graph
from Node import Node
import asyncio


def main():
    conns = [
        Connection(Node("a"), Node("b"), lambda x: x+1),
        Connection(Node("a"), Node("c"), lambda x: x),
        Connection(Node("b"), Node("e"), lambda x: 2),
        Connection(Node("c"), Node("e"), lambda x: x+2),
    ]
    (paths, lens) = asyncio.run(Graph(conns).find_path_for_population("a", "e", 5))
    print(paths, sum(lens)/len(lens))


if __name__ == "__main__":
    main()
