import math 
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ITEMS", help="enter number of circles",action="store", type=int)
parser.add_argument("-r", "--RADIUS", help="enter radius for all the circles",action="store", type=int)
parser.add_argument("-min_radius", "--MIN_RADIUS", help="enter min rad of circles",action="store",type=int)
parser.add_argument("-max_radius", "--MAX_RADIUS", help="enter max rad of circles",action="store",type=int)
parser.add_argument("-b", "--BOUNDARY_FILE", help="enter boundaries", type=argparse.FileType('r'), action="store")
parser.add_argument("-s", "--SEED", help="enter seed", action="store", type=int)
parser.add_argument("output_file", help="name of output file", type=argparse.FileType('w'))
args = parser.parse_args()

def format(value):
    return "%.2f" % value

def save_in_file(x,y,r):
    out_string = ""
    out_string += str(format(x))
    out_string += " " + str(format(y))
    out_string += " " + str(r)
    out_string += "\n"
    args.output_file.write(out_string)

def tangent_circles(cm,cn,r1,r2,r):
    dx=cn[0]-cm[0]
    dy=cn[1]-cm[1]
    d=math.sqrt(dx**2 + dy**2)
    k1=r1+r
    k2=r2+r
    l= (k1*k1 - k2*k2 + d*d)/(2*d*d)
    e = math.sqrt((k1*k1)/(d*d) - l*l)
    kx= cm[0] + l*dx - e*dy
    ky=cm[1]  + l*dy + e*dx
    kx=round(kx,2)
    ky=round(ky,2)
    return (kx,ky)

def distance_from_line(u,n,c):
    l = (u[0]-n[0])*(u[0]-n[0]) + (u[1]-n[1])*(u[1]-n[1])
    if l == 0:
        d = math.sqrt((u[0]-c[0])*(u[0]-c[0]) + (u[1]-c[1])*(u[1]-c[1]))
    else:
        t = (c[0]-u[0])*(n[0]-u[0]) + (c[1]-u[1])*(n[1]-u[1])
        t = t/l 
        t = max(0,min(1,t))
        px=u[0] + t*(n[0]-u[0])
        py=u[1] + t*(n[1]-u[1])
        d = math.sqrt((px-c[0])*(px-c[0]) + (py-c[1])*(py-c[1]))
        d = round(d,2)
    return d

def circle(x1, y1, x2, y2, r1, r2): 
    distSq = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    radSumSq = (r1 + r2) 
    distSq=round(distSq,2)
    radSumSq=round(radSumSq,2)
    if distSq < radSumSq: 
        return True
    else:
        return False  

def distance_from_start(x1,y1):
    distance = math.sqrt((x1 - 0) * (x1 - 0) + (y1 - 0) * (y1 - 0))
    distance = round(distance,2)
    return distance

def find_cm(metopo):
    i =0
    min = 1
    indicator=0
    for i in range(len(metopo)-1):
        dist=distance_from_start(metopo[i][0],metopo[i][1])
        if dist<min:
            min = dist
            indicator = i
    cm = metopo[indicator]
    return cm

def position(cm,cn,cj,metopo):
    x=cn
    y=0
    calculator = 0
    result = 0
    while y!=cm:
        y = graph[x]
        calculator = calculator + 1
        if y==cj:
            result = calculator
            calculator = 0
        x = y
    if result > (len(metopo) - result): #-1
        return True #prin apo cm
    else:
        return False #meta apo cn

def remove_circles(cj,cn,metopo):
    x = cj
    l=[]
    while graph[x]!=cn:
        y = graph[x]
        metopo.remove(y)
        l.append(y)
        x = y
    for it in l:
        graph.pop(it)

def tang(metopo,c):
    h=0
    boo=False
    circles=[]
    while h <len(metopo):
        boo = circle(metopo[h][0], metopo[h][1],c[0], c[1], r1, r2)
        if boo==True:
            circles.append(metopo[h])
        h=h+1
    return circles 

def check_circle_line(array,c):
    r=10
    temn=0
    for i in range(len(array)):
        d=distance_from_line(array[i][0],array[i][1],c)
        if d-r>0:
            temn=temn+1
    return temn

def social_dist(items,r):
    cm=(0,0)
    save_in_file(cm[0],cm[1],r1)
    cn=(r1+r2,0)
    save_in_file(cn[0],cn[1],r2)
    graph[cn] = cm
    metopo = [cm]
    metopo.append(cn)
    cj=0
    saved=2
    while saved != items: 
        c = tangent_circles(cm,cn,r1,r2,r)
        circles=tang(metopo,c)
        if len(circles)==1:
            cj=circles[0]
            if position(cm,cn,cj,metopo)==True:
                remove_circles(cj,cn,metopo)
                cm = cj
                graph[cm]=c
                graph[c]=cn
            else:
                remove_circles(cm,cj,metopo)
                cn = cj
        else:
            metopo.append(c)
            graph[cm]=c
            graph[c]=cn    
            save_in_file(c[0],c[1],r)
            saved=saved+1
            cm=find_cm(metopo)
            cn = graph[cm]
    return saved

if args.ITEMS and args.RADIUS:
    items=args.ITEMS
    radius = args.RADIUS
    r1=radius
    r2=radius
    graph={}
    print(social_dist(items,radius))

if args.BOUNDARY_FILE and args.ITEMS and args.RADIUS:
    array=[]
    i=0
    for line in args.BOUNDARY_FILE:
        fields = line.split()
        array.append(fields[0])
        array.append(fields[1])
        array.append(fields[2])
        array.append(fields[3])
    ar=[]
    i=0
    k=0
    while i !=len(array):
        ar[k]=(float(array[i]),float(array[i+1]))
        i = i+2
        k=k+1
    temn=0
    aray=ar
    items=args.ITEMS
    radius = args.RADIUS
    r1=radius
    r2=radius
    graph={}
    print(social(items,radius))

if (args.ITEMS) and (args.MIN_RADIUS) and (args.MAX_RADIUS) and (args.SEED or not args.SEED):
    items=args.ITEMS
    random.seed(args.SEED)
    min_rad=args.MIN_RADIUS
    max_rad=args.MAX_RADIUS
    r1 = random.randint(min_rad, max_rad)
    r2 = random.randint(min_rad, max_rad)
    graph={}
    print(social_dist(items,random.randint(min_rad, max_rad)))

def social(items,r):
    dead=[]
    cm=(0,0)
    save_in_file(cm[0],cm[1],r1)
    cn=(r1+r2,0)
    save_in_file(cn[0],cn[1],r2)
    graph[cn] = cm
    metopo = [cm]
    metopo.append(cn)
    cj=0
    saved=2
    start_cm=(0,0)
    while saved != items: 
        c = tangent_circles(cm,cn,r1,r2,r)
        circles=tang(metopo,c)
        if len(circles)==1:
            cj=circles[0]
            if position(cm,cn,cj,metopo)==True:
                remove_circles(cj,cn,metopo)
                #graph.pop(cm)
                cm = cj
                graph[cm]=c
                graph[c]=cn
            else:
                remove_circles(cm,cj,metopo)
                cn = cj
        else:
            temn=check_circle_line(aray,c)
            if temn==0:
                metopo.append(c)
                graph[cm]=c
                graph[c]=cn    
                save_in_file(c[0],c[1],r)
                saved=saved+1
                cm=find_cm(metopo)
                cn = graph[cm]
                start_cm=cm
            else: #(20.00, 103.92)
                metopo.remove(start_cm)
                dead.append(start_cm)
                cm=find_cm(metopo)
                cn = graph[cm]
                start_cm=cm
    return saved

