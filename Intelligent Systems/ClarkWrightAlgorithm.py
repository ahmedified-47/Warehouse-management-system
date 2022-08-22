from array import array
from audioop import reverse
import imp
import operator
from os import remove
from platform import node
from pyclbr import Class
import random
import functools
import itertools
import collections
import typing 
import math
import dataclasses

def biased_randomisation(alpha, beta):
    "This method carries out biased randomisation selection over certain list."
    "f(x) = (1 - beta) ^ x -- quasi geometric distribution"
    "This priortises the first element in the list."
    "This method will return the element picked at each iteration"
    list = len(array) # A list of options sorted from best to worst
    options = list(array)
    for _ in range(list):
        index = int(math.log(random.random(), 1.0 - beta)) % len(options)
        yield options.pop(index) # popping the index out --- no fucking idea what i'm doing right now xd
        
class Route(object): # Insrance of this class represents a route made by sequence of edges
    def __init__(self , edges = None):
        self.edges = edges or collections.deque()
        self.cost = sum(edge.cost for edge in self.edges)
        
    @property
    def first_node(self):
        return self.edges[0].destination # returning the first node visted after the depot
    
    @property 
    def last_node(self):
        return self.edges[-1].destination # returning the last node visited before coming back home;)
    
    def popLeft(self): # remove the first edge from the route & update costs
        pop_out = self.edges.popleft()
        self.cost -= pop_out.cost
        
    def popRight(self): # remove the last edge from the route & update costs
        pop_out = self.edges.pop()
        self.cost -= pop_out.cost
        
    def extend(self, edges): # update the cost and add new edges to route
        self.edges.extend(edges)# does it has to do anything with the price of tea in Antartica?
        self.cost += sum(edge.cost for edge in edges)
    
    def append(self, edge): # adding new edge to the route and automatically updates the cost too.
        self.edges.append(edge)
        self.cost += edge.cost
        
    def __repr__(self):
        return str(list(self.edges)) # I'm dead now going to sleep its 6 AM
    
    @dataclasses.dataclass(repr= True , frozen= True)
    class CWSConfiguration: # instance of this class represents the configuration of the parametres
        # can be passed to heauristic or call method ---- I don't know yet does that make me dumb?
        biased : bool = True # if ture biased randomisation is used. Callable method is passed and biased function is used
        reverse : bool = True # if true the possibility to reverse the routes we are going to merge is considered
        biasedFunction : typing.Callable = biased_randomisation # in case biased randomisation is required
        meta_heauristic : bool = False # if true more solutions are generated or if false then return single solution
        start : typing.Tuple[typing.List[Route], int] = None # start solution (generated with different method) metaheuritic starts from here
        max_iteration : int = 1000 # max number of solutions to explore in case of meta heauristic
        max_no_imp : int = 500  
        max_cost : float = float('inf')  # max cost of route that makes it feasible
        min_cost : float = float('-inf') # minimum number of routes allowed
        
        class ClarkWrightSavings(object): # represent Clark Wright Heauristic implementation
            def __init__(self, nodes, edges):
                self.nodes = nodes # the nodes to visit
                self.edges = edges # the edges connecting the nodes
                
            @staticmethod 
            def savings_list(edges): # edges is the list of edges
                # Generates saving list by simply sorting them for decreasing saving value
                return sorted(edges, key=operator.attrgetter("saving", reverse = True)) 
                
            @staticmethod
            def _reversed(route):
                # This method is used to instantiate and return a new route
                return Route(collections.deque(reversed([e.inverse for e in route.edges])))
            
            def heuristic(self, config):
                #Clark right saving algorithm is implemented
                edges = self.edges
                nodes = self.nodes
                biased = config.biased
                biasedfunc = config.biasedfunc
                reverse = config.reverse
                maxcost = config.maxcost
                minroutes = config.minroutes
                routes = list()
                
            # creating dummy solution
            for node in nodes:
                 rt = Route(collections.deque([node.dn_edge, node.nd_edge]))
                 node.route = rt
                 routes.append(rt)
                 
            # Generating the savings list with eventual biased randomisation
            savings_list = self.savings_list(edges)
            savings_iterator = savings_list if not biased else biasedFunction(savings_list)
            
            # starting iterative merging process
            for edge in savings_iterator
                # Check if minimum number has been reached
                if len(routes) <= minroutes:
                    return routes, sum(r.cost for r in routes)
            
            # Generates the savings list with eventual biased randomisation
            savings_list = self.savings_list(edges)
            
