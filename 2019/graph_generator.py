import argparse
import random


def generate_graph(nrnodes, nrextraedges, minedgecost, maxedgecost):
    start_priority = random.randint(1, 25)
    priorities = [10*(k+start_priority) for k in range(nrnodes)]
    random.shuffle(priorities)
    for k in range(len(priorities)):
        priorities[k] = [k, priorities[k]]
    
    adjmatrix = [[0 for _ in range(nrnodes)] for _ in range(nrnodes)]
    
    edges = []
    for j in range(nrnodes-1):
        cost = random.randint(minedgecost, maxedgecost)
        edges.append([j, j+1, cost])
        adjmatrix[j][j+1] = 1
        adjmatrix[j+1][j] = 1
    
    for j in range(nrextraedges):
        cost = random.randint(minedgecost, maxedgecost)
        while True:
            k1 = random.randint(0, nrnodes-1)
            k2 = random.randint(0, nrnodes-1)
            if k2 != k1 and adjmatrix[k1][k2] == 0:
                break
        edges.append([k1, k2, cost])
        adjmatrix[k1][k2] = 1
        adjmatrix[k2][k1] = 1
        
    random.shuffle(priorities)
    
    fromnode = random.randint(0, nrnodes-1)
    while True:
        tonode = random.randint(0, nrnodes-1)
        if tonode != fromnode:
            break
    
    return priorities, edges, fromnode, tonode

    
def print_graph(graph, filename):
    nodes, edges, fromnode, tonode = graph
    
    network = [nodes, edges]
    string = "retea(R) :- R = {0}.\nfrom({1}).\nto({2}).\n".format(network, fromnode, tonode)
    
    with open(filename, "w") as file:
        file.write(string)
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Graph generator for STP')
    parser.add_argument('--minnodes', type=int, required=True)
    parser.add_argument('--maxnodes', type=int, required=True)
    parser.add_argument('--minextraedges', type=int, required=True)
    parser.add_argument('--maxextraedges', type=int, required=True)
    parser.add_argument('--minedgecost', type=int, required=True)
    parser.add_argument('--maxedgecost', type=int, required=True)
    parser.add_argument('--count', type=int, required=True)
    parser.add_argument('--filename', required=True)
    parser.add_argument('--startindex', type=int, required=True)
    args = parser.parse_args()
    
    for i in range(args.count):
        index = i + args.startindex
        filename = "{0}{1}.txt".format(args.filename, index)
        
        nrnodes = random.randint(args.minnodes, args.maxnodes)
        nrextraedges = random.randint(args.minextraedges, args.maxextraedges)
        minedgecost = args.minedgecost
        maxedgecost = args.maxedgecost
        
        graph = generate_graph(nrnodes, nrextraedges, minedgecost, maxedgecost)
        print_graph(graph, filename)
        