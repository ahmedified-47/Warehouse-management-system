import os
import sys

def __init__(self, id, to_depot, from_depot):
    self.id = id
    
    # Attributes used by CWS algorithm
    self.route = None
    self.to_depot = to_depot
    self.from_depot = from_depot
    
    def __repr__(self):
        return str(self.id)
    
