class Node:
    def __init__(self, qr, x, y):
        self.x = x
        self.y = y
        self.qr = qr
        self.is_free = True

    def setState(self, is_free):
        self.is_free = is_free

    def getState(self):
        return self.is_free

class Edge:
    def __init__(self, node_a, node_b):
        self.nodes = [node_a, node_b]
        self.is_free = True

    def setState(self, is_free):
        self.is_free = is_free

    def getState(self):
        return self.is_free

class WarehouseFloor:
    def __init__(self):
        with open("warehouse_map", "r") as warehouse_map:
            self.raw_map = warehouse_map.readlines()
        

if __name__ == "__main__":
    a = WarehouseFloor()