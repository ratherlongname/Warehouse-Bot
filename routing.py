from __future__ import print_function
import matplotlib.pyplot as plt

class AStarGraph(object):
    #Define a class board like grid with two barriers

    def __init__(self, warehouse_map):
        if warehouse_map is '':
            warehouse_map = "warehouse_map"
        self.barriers, self.x_max, self.y_max = self.read_map_file(warehouse_map)
        # list of tuples (x, y) co-ordinates of points that are blocked eg. [(2,4), (2,5)]

    def add_barrier(self, xy):
        x, y = xy
        if x < 0 or x > self.x_max or y < 0 or y > self.y_max:
            raise ValueError("Barrier co-ordinates are outside map")
        elif (x, y) not in self.barriers:
            self.barriers.append((x, y))
        return
    
    def remove_barrier(self, xy):
        x, y = xy
        if x < 0 or x > self.x_max or y < 0 or y > self.y_max:
            raise ValueError("Barrier co-ordinates are outside map")
        elif (x, y) in self.barriers:
            self.barriers.remove((x, y))
        return

    def read_map_file(self, warehouse_map):
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
                if node is 'N':
                    barriers.append((x, y))
        return barriers, x_max, y_max

    def heuristic(self, start, goal):
        #Use Manhattan distance heuristic
        D = 1
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return D * (dx + dy)

    def get_vertex_neighbours(self, pos):
        n = []
        # Moves allowed- only four directions
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            x2 = pos[0] + dx
            y2 = pos[1] + dy
            if x2 < 0 or x2 > self.x_max or y2 < 0 or y2 > self.y_max:
                continue
            n.append((x2, y2))
        return n

    def move_cost(self, a, b):
        if b in self.barriers:
            return 100 #Extremely high cost to enter barrier squares
        return 1 #Normal movement cost

    def print_map(self):
        plt.plot([v[0] for v in self.barriers], [v[1] for v in self.barriers], 'ro')
        plt.xlim(-1, self.x_max+1)
        plt.ylim(self.y_max+1, -1)
        plt.show()
        return

def AStarSearch(start, end, graph):

    G = {} #Actual movement cost to each position from the start position
    F = {} #Estimated movement cost of start to end going via this position

    #Initialize starting values
    G[start] = 0
    F[start] = graph.heuristic(start, end)

    closedVertices = set()
    openVertices = set([start])
    cameFrom = {}

    while len(openVertices) > 0:
        #Get the vertex in the open list with the lowest F score
        current = None
        currentFscore = None
        for pos in openVertices:
            if current is None or F[pos] < currentFscore:
                currentFscore = F[pos]
                current = pos

        #Check if we have reached the goal
        if current == end:
            #Retrace our route backward
            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            return path, F[end] #Done!

        #Mark the current vertex as closed
        openVertices.remove(current)
        closedVertices.add(current)

        #Update scores for vertices near the current position
        for neighbour in graph.get_vertex_neighbours(current):
            if neighbour in closedVertices:
                continue #We have already processed this node exhaustively
            candidateG = G[current] + graph.move_cost(current, neighbour)

            if neighbour not in openVertices:
                openVertices.add(neighbour) #Discovered a new vertex
            elif candidateG >= G[neighbour]:
                continue #This G score is worse than previously found

            #Adopt this G score
            cameFrom[neighbour] = current
            G[neighbour] = candidateG
            H = graph.heuristic(neighbour, end)
            F[neighbour] = G[neighbour] + H

    raise RuntimeError("A* failed to find a solution")

def draw_route(graph, route):
    plt.plot([v[0] for v in route], [v[1] for v in route])
    plt.plot([v[0] for v in graph.barriers], [v[1] for v in graph.barriers], 'ro')
    plt.xlim(-1, graph.x_max+1)
    plt.ylim(graph.y_max+1, -1)
    plt.show()
    return

def menu():
    main_menu = ['q to quit',
                'g to go from a to b',
                'a to add barrier',
                'r to remove barrier',
                's to show map']
    map_filename = input("Give filename of warehouse map (default=warehouse_map):\n")
    graph = AStarGraph(map_filename)

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
            result, cost = AStarSearch(start, end, graph)
            print ("Route: {}\nCost: {}".format(result, cost))
            draw_route(graph, result)
        elif choice is 'a':
            print("Enter barrier point to add (x,y):")
            barrier = tuple([int(x) for x in input().split(',')])
            graph.add_barrier(barrier)
        elif choice is 'r':
            print("Enter barrier point to remove (x,y):")
            barrier = tuple([int(x) for x in input().split(',')])
            graph.remove_barrier(barrier)
        elif choice is 's':
            graph.print_map()
    return

if __name__=="__main__":
    menu()