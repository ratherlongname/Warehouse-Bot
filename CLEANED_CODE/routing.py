# import matplotlib.pyplot as plt


class AStar():
    # Define a class board like grid with two barriers

    def __init__(self, warehouse_map):
        if warehouse_map == '':
            warehouse_map = "warehouse_map"
        self.barriers, self.x_max, self.y_max = self.read_map_file(
            warehouse_map)
        # list of tuples (x, y) co-ordinates of points that are blocked eg. [(2,4), (2,5)]

    def read_map_file(self, warehouse_map): # pylint: disable=no-self-use
        with open(warehouse_map, 'r') as map_file:
            raw_map_data = map_file.readlines()

        map_data = [line.split() for line in raw_map_data]
        x_max = int(map_data[0][-1])
        y_max = int(map_data[-1][0])
        map_data.pop(0)
        for line in map_data:
            line.pop(0)
        barriers = []
        for y, line in enumerate(map_data):
            for x, node in enumerate(line):
                if node == 'N':
                    barriers.append((x, y))
        return barriers, x_max, y_max

    def heuristic(self, start, goal): # pylint: disable=no-self-use
        # Use Manhattan distance heuristic
        D = 1
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return D * (dx + dy)

    def get_vertex_neighbours(self, pos):
        n = []
        # Moves allowed- only four directions
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x2 = pos[0] + dx
            y2 = pos[1] + dy
            if x2 < 0 or x2 > self.x_max or y2 < 0 or y2 > self.y_max:
                continue
            n.append((x2, y2))
        return n

    def move_cost(self, a, b):# pylint: disable=unused-argument
        if b in self.barriers:
            return 100  # Extremely high cost to enter barrier squares
        return 1  # Normal movement cost

    def search_path(self, start, end):

        G = {}  # Actual movement cost to each position from the start position
        F = {}  # Estimated movement cost of start to end going via this position

        # Initialize starting values
        G[start] = 0
        F[start] = self.heuristic(start, end)

        closedVertices = set()
        openVertices = set([start])
        cameFrom = {}

        while len(openVertices) > 0:
            # Get the vertex in the open list with the lowest F score
            current = None
            currentFscore = None
            for pos in openVertices:
                if current is None or F[pos] < currentFscore:
                    currentFscore = F[pos]
                    current = pos

            # Check if we have reached the goal
            if current == end:
                # Retrace our route backward
                path = [current]
                while current in cameFrom:
                    current = cameFrom[current]
                    path.append(current)
                path.reverse()
                return path, F[end]  # Done!

            # Mark the current vertex as closed
            openVertices.remove(current)
            closedVertices.add(current)

            # Update scores for vertices near the current position
            for neighbour in self.get_vertex_neighbours(current):
                if neighbour in closedVertices:
                    continue  # We have already processed this node exhaustively
                candidateG = G[current] + self.move_cost(current, neighbour)

                if neighbour not in openVertices:
                    openVertices.add(neighbour)  # Discovered a new vertex
                elif candidateG >= G[neighbour]:
                    continue  # This G score is worse than previously found

                # Adopt this G score
                cameFrom[neighbour] = current
                G[neighbour] = candidateG
                H = self.heuristic(neighbour, end)
                F[neighbour] = G[neighbour] + H

        raise RuntimeError("A* failed to find a solution")


if __name__ == "__main__":
    example = '''
        def menu():
            main_menu = ['q to quit',
                        'g to go from a to b']
            map_filename = input(
                "Give filename of warehouse map (default=warehouse_map):\n")
            graph = AStar(map_filename)

            while True:
                print("\tWAREHOUSE ROUTE TEST MENU")
                for option in main_menu:
                    print(option)

                choice = input()
                if choice is 'q':
                    print("Exiting...")
                    return
                elif choice is 'g':
                    print("Enter starting point (x,y):")
                    start = tuple([int(x) for x in input().split(',')])
                    print("Enter end point (x,y):")
                    end = tuple([int(x) for x in input().split(',')])
                    result, cost = graph.search_path(start, end)
                    print("Route: {}\nCost: {}".format(result, cost))
                    plt.plot([v[0] for v in result], [v[1] for v in result])
                    plt.plot([v[0] for v in graph.barriers], [v[1]
                                                            for v in graph.barriers], 'ro')
                    plt.xlim(-1, graph.x_max+1)
                    plt.ylim(graph.y_max+1, -1)
                    plt.show()
    '''
    raise Exception("This is not a top level module")
