from distutils.command.config import config
from operator import truediv
from pyclbr import Class
import os
import cws
import random
import math
import itertools

def distance (a,b):
    return int(math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2)))

def random_customer(id):
    return Customer(id, (random.randint(0,100), random.randint(0,100)))

def getting_routes(customers):
    routes = []
    for i, j in itertools.combinations(customer, 2):
        saving = i.node_edge.cost + j.node_edge.cost - distance(i.a, j.b)
        cost = distance(i.a, j.b)
        r = Route(i, j, saving, cost)
        r_inverse = Route(j, i, saving, cost)
        r.inverse = r_inverse
        r_inverse.inverse = r
        routes.append(r)
    return tuple(routes)

depot = (0,0)

Class Route (cws.Edge):
    pass

Class Customer (cws.Node):
      def __init__(self, id, c):
          self.c = c
          depot_edge = Route("depot", self, 0, cost = distance(depot, c))
          node_edge = Route(self, "depot", 0, cost = distance(c,depot))
          depot_edge.inverse = node_edge
          node_edge.inverse = depot_edge
          super(Customer, self).__init__(id, depot_edge, node_edge)
          customers = tuple(random_customer(i) for i in range(20))
          routes = getting_routes(customers)
          
     if (__name__ = "__main__"):
         print("Program:", end= "")
         config = cws.CWSConfiguration(
         biased = True,
         max_iteration = 1000,
         max_no_imp = 500,
         reverse = True,
         meta_heuristic = True,
         start = None,
         min_routes = 5,
         max_cost = float("inf"),
         )
         
         solution = cws.ClarkWrightSavings(nodes = customers, edges = routes)
         result, cost = solution.__call__(config)
         print("It's done!")
         
         for res in result:
             print(res)