import argparse
from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--verbose", help="program uses max node's degree as criterion to delete node from graph",action="store_true")
parser.add_argument("-r", "--verbosity", help="program uses collective influence to delete node from graph",action="store_true", default=0)
parser.add_argument("RADIUS", help="RADIUS", type=int, nargs='*')
parser.add_argument("num_nodes", help="number of nodes to be deleted from graph", type=int)
parser.add_argument("filename", help="name of input file")
args = parser.parse_args()
num_nodes = args.num_nodes

graph = {}
nodes = []
with open(args.filename) as filename:
    for line in filename: 
        data = line.split()
        nodes.append(int(data[0]))
        nodes.append(int(data[1]))
        parts = [int(x) for x in line.split()]
        if len(parts) != 2:
            continue
        if parts[0] not in graph:
            graph[parts[0]] = []
        if parts[1] not in graph:
            graph[parts[1]] = []
        graph[parts[0]].append(parts[1])
        graph[parts[1]].append(parts[0])

def remove_from_graph(k):
    for n in graph[k]:
        graph[n].remove(k)
    graph.pop(k)
    return graph

def create_node_list():
    list1 = sorted(graph.keys())
    return list1

def create_degree_list():
    list2=[]
    for n in sorted(graph.keys()):
        list2.append(len(graph[n]))
    return list2

def fisrt_way():
    list1=create_node_list()
    list2=create_degree_list()
    index = list2.index(max(list2))
    c = max(list2)
    k=list1[index] 
    remove_from_graph(k)
    print(list1[index], c)

def bfs(g, node,r):
    q = deque()
    visited = [ False for k in range(len(g.keys()) +1) ]
    inqueue = [ False for k in range(len(g.keys()) +1) ]
    for nod in g[node]:
        q.appendleft(nod)
        inqueue[nod] = True
    visited[node]=True
    bub=[]
    bub=q
    rad=1
    while not (rad == r):
        for c in list(bub):
            q.pop()
            inqueue[c] = False
            visited[c] = True
            for v in g[c]:
                if not visited[v] and not inqueue[v]:
                    q.appendleft(v)
                    inqueue[v] = True
        rad=rad+1
        bub=q
    return q

def remove_node(k):
    for n in graph[k]:
        graph[n].remove(k)
    graph[k]=[]
    return graph

def find_ci(graph,ball,n):
    sum=0
    for b in ball:
        sum=(len(graph[b])-1)+sum
    ci=(len(graph[n])-1)*sum
    return ci

def update_affected(k):
    affected=[]
    i=1
    while i!=r+2:
        ball=bfs(graph,k,i)
        affected.append(ball)
        i=i+1
    return affected
    
def second_way(c_l):
    list1=create_node_list()
    list2=c_l
    index = list2.index(max(list2))
    c = max(list2)
    k=list1[index]
    affected=update_affected(k)
    graph=remove_node(k)
    ci_list[k-1]=0
    print(list1[index], c)
    i=0
    while i!=len(affected):
        for aff in affected[i]:
            bal=bfs(graph,aff,r)
            new_ci=find_ci(graph,bal,aff)
            ci_list[aff-1]=new_ci
        i=i+1
    
def collective_influence():
    ci_list=[]
    for node in sorted(graph.keys()):
        ball=bfs(graph,node,r)
        ci=find_ci(graph,ball,node)
        ci_list.append(ci)
    return ci_list

i=0
if args.verbose:
    while (i!=num_nodes):
        fisrt_way()
        i=i+1
else:
    if args.verbosity:
        radius = args.RADIUS
        r = radius[0]
        ci_list=collective_influence()
        while (i!=num_nodes):
            second_way(ci_list)
            i=i+1
