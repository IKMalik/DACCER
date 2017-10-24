class Matrix:  # Class that creates adjacency matrix for displaying graph.

    def __init__(self):
        self.graph = {}  # graph to be displayed
        self.matrix = []  # list that will contain the adjacency matrix

    def create_matrix(self):
        keys = sorted(self.graph.keys())  # ordering of keys in graph for use in matrix table
        self.matrix.append(['-'] + keys)  # column headers
        for node in keys:
            row = [node]  # create a row[list] for each key in the graph
            for neighbours in keys: # for every node in the graph

                if node == neighbours:  # check if the nodes are same
                    row.append('-')  # if same then insert blank
                elif neighbours in self.graph[node]:  # if neighbour node is actually a neighbour of the current node
                    row.append(self.graph[node][neighbours])  # insert the distance from the node to the neighbour
                else:
                    row.append('-')  # the neighbour node is not in the neighbours of source so blank is inserted
            self.matrix.append(row)  # Add completed row to matrix
        return self.display_matrix()  # call method for display graph formatting

    def display_matrix(self): # function to display graph as formatted string string

        display_matrix = [map("{:^7}".format, line) for line in self.matrix] # map applies formatting every list in -
                                                                             # matrix
                                                                             # ^7 is spacing between elements

        start = "(["  # opening part of string
        end = "])"  # last part of string

        lines = ["[{}]".format(" ".join(array)) for array in display_matrix] # joins the formatted graph
        line_prefix = ",\n" + " " * len(start)
        data = line_prefix.join(lines)

        return start + data + end  # return the matrix
