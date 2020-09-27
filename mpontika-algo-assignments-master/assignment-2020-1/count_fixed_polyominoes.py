import sys
import pprint

if len(sys.argv)>2:
    p=int(sys.argv[2])
else:
    p =int(sys.argv[1])

f=-p + 1
d =p
g = {}

for y in range(0,p):
    for x in range(f,d):
        if y==0 and x<0:
            continue
        g[(x,y)] = []   
    d -= 1
    f += 1

l=[] #adjacency list of dictionary's nodes

for c in sorted(g.keys()):  
    for k in sorted(g.keys()):
        if (c[0]-k[0]==-1 and c[1]==k[1]):
            l.insert(3,k)
        if (c[1]-k[1]==-1 and c[0]==k[0]):
            l.insert(2,k)
        if (c[0]-k[0]==1 and c[1]==k[1]):
            l.insert(1,k)
        if (c[1]-k[1]==1 and c[0]==k[0]): 
            l.insert(0,k)
    l.reverse()
    g[c]= l
    l=[]
           
if sys.argv[1]=='-p': 
    pprint.pprint(g)

untried = {(0,0)}
n=p
c=0
a = 0
cp= [] #current polyominoe

def AddOne(c):
    c=c+1
    return c

def Count_Fixed_Polyominoes(g,untried,n,cp,c):
    while len(untried) != 0:
        u = untried.pop()
        cp.append(u)
        if len(cp) == n:
            c = AddOne(c)
        else:
            new_neighbours = set()
            for v in g[u]:
                i=0
                boo = v in untried
                foo= v in cp
                for node in cp:
                    if v not in g[node]:
                        i +=1 
                if (boo== False) and (foo==False) and (i==len(cp)-1):
                    new_neighbours.add(v) 
            new_untried = untried.union(new_neighbours)
            c = Count_Fixed_Polyominoes(g, new_untried,n,cp,c)
        cp.remove(u)  
    return c

print(Count_Fixed_Polyominoes(g,untried,n,cp,c))

