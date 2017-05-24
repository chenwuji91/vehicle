#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''

import networkx as nx
import read
import tools

intersection = read.readLukou()
adj = read.readAdj()
def edge_distance(point1, point2):
    p_info0 = intersection[int(point1)]
    p_info1 = intersection[int(point2)]
    distance = tools.calculate(p_info0[0], p_info0[1], p_info1[0], p_info1[1])
    return distance

def graphGenerate():
    G = nx.DiGraph()
    for eachpair in adj:
        distance = edge_distance(eachpair[0], eachpair[1])
        G.add_edge(eachpair[0], eachpair[1], weight = distance)
    print "有向带权图加载完成"
    return G

G = graphGenerate()

def nearestPath(point1,point2):
    try:
        return nx.dijkstra_path(G, int(point1) , int(point2))

    except:
        print 'Warning! Path unreachable! Return Wrong Result'
        return [int(point1),int(point2)]

def nearestPathLen(point1,point2):
    try:
        return nx.dijkstra_path_length(G, int(point1) , int(point2))
    except:
        print 'Warning! Path unreachable! Return Wrong Result'
        return 123456789
