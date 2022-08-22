import abc #not used so far
class edge(abc.ABC): # has attributes needed to work as the edge of the graph
    def __init__(self, depot, destination, saving, cost = 0):
        self.depot = depot
        self.destination = destination
        self.saving = saving # The saving value associated to this edge
        self.cost = cost # the cost associated to this edge
        self.inverse = None # the inverse edge
        
    def __repr__(self) -> str:
        return  f"({self.depot} -> {self.destination})"
        
