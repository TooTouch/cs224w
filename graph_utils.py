import snap
import numpy as np 
import pandas as pd 

def calc_self_edges(G):
    """
    Calculate the number of self-edges in a graph
    
    Args: 
    - G: Graph class. i.e. snap.PNGraph

    Return:
    - nb_self_edges: the number of self-edges
    """

    nb_self_edges = 0
    for EI in G.Edges():
        if EI.GetSrcNId() == EI.GetDstNId():
            nb_self_edges += 1
    return nb_self_edges


def calc_undirected_edges(G):
    """
    Calculate the number of undirected-edges in a graph

    Args:
    - G: Graph class. i.e. snap.PNGraph

    Return:
    - len(undirected_edges): the number of undirected-edges in a graph
    """

    undirected_edges = set()
    
    for EI in G.Edges():
        u = EI.GetSrcNId()
        v = EI.GetDstNId()
        if ((u,v) not in undirected_edges) and ((v,u) not in undirected_edges) and (u!=v):
            undirected_edges.add((u,v))

    return len(undirected_edges)


def calc_reciprocated_edges(G):
    """
    Calculate the number of reciprocated-edges in a graph

    Args:
    - G: Graph class. i.e. snap.PNGraph

    Return:
    - int(len(reciprocated_edges)/2): the number of reciprocated_edges

    """
    reciprocated_edges = set()
    
    for EI in G.Edges():
        u = EI.GetSrcNId()
        v = EI.GetDstNId()
        reciprocated_edges.add((u,v))
        
        if (u==v):
            reciprocated_edges.remove((u,v))
    
    for EI in G.Edges():
        u = EI.GetSrcNId()
        v = EI.GetDstNId()
        if (u!=v) and (v,u) not in reciprocated_edges:
            reciprocated_edges.remove((u, v))
            
    return int(len(reciprocated_edges) / 2)


def create_erdos_renyi_random_graph(N: int, E: int):
    """
    Erdős-Rényi Random Graph
    
    This is a undirected graph that has nodes connected with random probability (binomial distribution)
    
    Args:
    - N : the number of nodes
    - E : the number of edges
    
    Return:
    - Undirected Random Graph that has N nodes and E edges
    """
    
    UG = snap.PUNGraph.New()
    p = 1/(N-1)
    
    nodes = range(N)
    for node in nodes:
        UG.AddNode(node)

    while UG.GetEdges() < E:
        for node in nodes:
            node_dst = np.random.binomial(n=N-1, p=p, size=1)[0]
            if node != node_dst: # self-edge (x)
                UG.AddEdge(node, int(node_dst))
            
            if UG.GetEdges() == E:
                break
        
    return UG


def create_small_world_random_graph(N: int, E: int, verbose=False):
    """
    Small-World Random Graph
    
    This is a undirected graph that has 3-steps as follow.
    - Step 1 : First, each node is connected to its two direct neighbors. Then, N edges is added in the graph.
    - Step 2 : Next, each node is connected to the neighbors of its neighbors. N edges is added in the graph as like before.
    - Step 3 : Finally, randomly select E-2N pairs of nodes not yet connected and add an edge between them.
    
    Args:
    - N : the number of nodes
    - E : the number of edges
    
    Return:
    - Undirected Random Graph that has N nodes and E edges
    
    """
    
    UG = snap.PUNGraph.New()
    
    nodes = range(N)
    
    for node in nodes:
        UG.AddNode(node)
    
    # step 1
    for node in nodes:
        if node == len(nodes)-1:
            UG.AddEdge(node, 0)
        else:
            UG.AddEdge(node, node+1)
    
    if verbose:
        print('the number of edges in step 1: ',UG.GetEdges())
    
    # step 2
    for node in nodes:
        if node == len(nodes)-2:
            UG.AddEdge(node, 0)
        elif node == len(nodes)-1:
            UG.AddEdge(node, 1)
        else:
            UG.AddEdge(node, node+2)
            
    if verbose:
        print('the number of edges in step 2: ',UG.GetEdges())
    
    # step 3
    while UG.GetEdges() < E:
        for node in nodes:
            node_dst = np.random.randint(low=0, high=len(nodes), size=1)[0]
            UG.AddEdge(node, int(node_dst))
            
            if UG.GetEdges() == E:
                break
                
    if verbose:
        print('the number of edges in step 2: ',UG.GetEdges())
            
    return UG