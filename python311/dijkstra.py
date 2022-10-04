import timeit
from functools import partial
from statistics import median

Graph = list[list[float]]

MAX_DISTANCE = 1e7


def min_dist(dist: list[float], processed: list[bool]) -> int:
    min_index = -1
    current_min = MAX_DISTANCE
    for index, value in enumerate(dist):
        if value < current_min and not processed[index]:
            current_min = value
            min_index = index
    return min_index


def dijkstra(graph: Graph, index: int = 0) -> list[float]:
    vertex_count = len(graph)
    dist = [MAX_DISTANCE] * vertex_count
    dist[index] = 0
    processed = [False] * vertex_count

    for _ in range(len(graph)):
        min_dist_vertex = min_dist(dist, processed)
        processed[min_dist_vertex] = True
        for current_vertex in range(vertex_count):
            if (
                graph[min_dist_vertex][current_vertex] > 0
                and not processed[current_vertex]
                and dist[current_vertex]
                > dist[min_dist_vertex] + graph[min_dist_vertex][current_vertex]
            ):
                dist[current_vertex] = (
                    dist[min_dist_vertex] + graph[min_dist_vertex][current_vertex]
                )
    return dist


def main() -> None:
    graph: list[list[float]] = [
        [0, 4, 0, 0, 0, 0, 0, 8, 0],
        [4, 0, 8, 0, 0, 0, 0, 11, 0],
        [0, 8, 0, 7, 0, 4, 0, 0, 2],
        [0, 0, 7, 0, 9, 14, 0, 0, 0],
        [0, 0, 0, 9, 0, 10, 0, 0, 0],
        [0, 0, 4, 14, 10, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 1, 6],
        [8, 11, 0, 0, 0, 0, 1, 0, 7],
        [0, 0, 2, 0, 0, 0, 6, 7, 0],
    ]

    result = timeit.repeat(partial(dijkstra, graph=graph), number=10000)
    print(f"Min: {min(result)}, Max: {max(result)}, Median: {median(result)}")


if __name__ == "__main__":
    main()
