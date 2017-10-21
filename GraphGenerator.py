
import random as rnd
import string as st
import sys as sy


class AbstractGraph:  # all graph types inherit from this base class

    def __init__(self):
        self.graph = {}  # dictionary to hold graph

    def setup_neighbours(self):
        raise NotImplementedError("abstract method must be overwritten by subclass")

    def setup_nodes(self):
        raise NotImplementedError("abstract method must be overwritten by subclass")


class ComplexGraph(AbstractGraph):  # class for graph that inherits from base class

    def setup_nodes(self):
        num_nodes = rnd.randint(6,10) #27 max , 6 lower as most exam questions have between 6-9 nodes
        for node in range(num_nodes):
            self.graph[st.ascii_lowercase[node]] = {}  # each node is assigned letter for identification

    def setup_neighbours(self):  # creates neighbours randomly for each source node
        for key in (self.graph.keys()):
            num_neighbours = rnd.randint(0, 1)   # 0 or 1 explained in documentation
            for neighbour in range(num_neighbours+1):
                neighbour = rnd.choice(list(self.graph.keys()))  # selcted random node as neighbour
                while neighbour == key:   # if neighbour is source node
                    neighbour = rnd.choice(list(self.graph.keys()))
                try:
                    if self.graph[key][neighbour] >= 0:  # check if neighbour already exists
                        pass  # if exists then skip it
                except KeyError: # if not exists then add
                    distance = rnd.randint(1, 100)  # if not exists , set it up both ways as a-b = b-a
                    self.graph[key][neighbour] = distance
                    self.graph[neighbour][key] = distance


