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
    L = len(array) # A list of options sorted from best to worst
    options = list(array)
    for _ in range(L):
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
        return self.edges[-1].origin # returning the last node visited before coming back home;)
    
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
            savings_iterator = savings_list if not biased else biasedfunc(savings_list)
            
            # starting iterative merging process
            for edge in savings_iterator:
                # Check if minimum number has been reached
                if len(routes) <= minroutes:
                    return routes, sum(r.cost for r in routes)
            
              # Get the routes connected by the currently considered edge
              origin = edge.origin
              destination = edge.destination
              i_route = edge.origin.route
              j_route = destination.dest.route
              
              # If routes are the same then next edge is considered
              if i_route == j_route:
                  continue
              
            # Check if extremes of edges are internat  consider the next edge
            if (origin != i_route.first_node and origin != i_route.last_node) or \
                (destination != j_route.first_node and destination != j_route.last_node):
                    continue
            # If merging is possible with no reversions
            if origin == i_route.last_node and destination == j_route.first_node:
                # If it's less than max cost of the route
                if i_route.cost + j_route.cost - edge.saving <= maxcost:
                 # remove the edges to the origin in merged routes
                 i_route.popright(); j_route.popleft()
                 # Building new route -- better roads xd
                 i_route.append(edge)
                 i_route.extend(j_route.edges)
                 # Update the reference to the route in the nodes
                 edge.destination.route = iroute
                 for e in itertools.islice(j_route.edges, 0, len(j_route.edges) - 1):
                     e.destination.route = iroute
                # Update the list of the routes
                  routes.remove(j_route)
                # Next edge is considered
                continue
            
            # If it is not possible to reverse the routes and the edges then continue
            # If the reversion of the routes is possible
            if reverse:
                # Intialise the revers edge
                r_edge, r_iroute, r_jroute, = edge, i_route, j_route
                # If both should be reversed reverse the edge
                if origin == i_route.first_node and destination == j_route.last_node
                redge = edge.inverse
                # Reverse the first route
                 elif origin != i_route.last_node and destination == j_route.first_node:
                    routes.remove(i_route)
                    r_iroute = self._reversed(i_route)
                    routes.append(r_iroute)                
                # Reverse the second route
                  elif origin == i_route.last_node and destination != j_route.first_node:
                    routes.remove(j_route)
                    rjroute = self._reversed(j_route)
                    routes.append(r_jroute)
                # If route cost doesn't exceed max cost
                if r_iroute.cost + r_jroute.cost - redge.saving <= maxcost:
                # Remove the edges to the origin in the merged routes
                r_iroute.popright(); r_jroute.popleft()
                # Build the new route 
                r_iroute.append(redge)
                r_iroute.extend(r_jroute.edges)
                # Update the reference to the route in the nodes
                for e in itertools.islice(r_iroute.edges, 0, len(r_iroute.edges) - 1):
                    e.destination.route = r_iroute
                # Update the list of the routes
                routes.remove(r_jroute)
                
                # return the solution found
                return routes, sum(r.cost for r in routes)
            
    def metaheuristic(self, starting_solution, config):
        #This method represents an Iterated Local Search in which
       # the Clarke Wright Savings heuristic is incorporated.
        #In order to generate a ifferent solution at each iteration,
        #the biased randomisation in the configuration should be activated
        #and a biasedfunc should be provided.
        
        # Initialise the solution we want to generate new solutions
        heuristic = functools.partial(self.heuristic, config)
        # Initialise the current best solution
        best, cost = starting_solution
        maxiter = config.maxiter
        maxnoimp = config.maxnoimp
        missed_improvements = 0
        # Starts the iterated the local search
        for _ in range(maxiter):
            # Generate new solution
            new_solution , new_cost = heauristic()
            missed_improvements += 1
            # Eventually updates the best
            if newcost < cost:
                best =  new_solution
                cost =  new_cost
                missed_improvements = 0
            # If maximum number of iterations exceeded
            if missed_improvements > maxnoimp:
                return best, cost
            # Return the best solution found at the end of the process
            return best, cost
        
        def __call__(self, config): # main function of the algorithm
            best, cost = self.heuritic(config)
            if config.metaheuristic:
                starting_solution = config.start or self.heuristic(config)
                best, cost = self.metaheuristic(starting_solution, config)
            return best,cost
