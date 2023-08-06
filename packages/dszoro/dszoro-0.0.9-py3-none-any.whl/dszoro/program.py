def splay():
    code = '''
class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None
    def other_name(self, level=0):
        print('\t' * level + repr(self.value))
        for child in self.children:
            child.other_name(level + 1)

class SplayTree:
    def __init__(self):
        self.root = None

    def maximum(self, x):
        while x.right != None:
            x = x.right
        return x

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != None:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None: #x is root
            self.root = y

        elif x == x.parent.left: #x is left child
            x.parent.left = y

        else: #x is right child
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != None:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None: #x is root
            self.root = y

        elif x == x.parent.right: #x is right child
            x.parent.right = y

        else: #x is left child
            x.parent.left = y

        y.right = x
        x.parent = y

    def splay(self, n):
        while n.parent != None: #node is not root
            if n.parent == self.root: #node is child of root, one rotation
                if n == n.parent.left:
                    self.right_rotate(n.parent)
                else:
                    self.left_rotate(n.parent)

            else:
                p = n.parent
                g = p.parent #grandparent

                if n.parent.left == n and p.parent.left == p: #both are left children
                    self.right_rotate(g)
                    self.right_rotate(p)

                elif n.parent.right == n and p.parent.right == p: #both are right children
                    self.left_rotate(g)
                    self.left_rotate(p)

                elif n.parent.right == n and p.parent.left == p:
                    self.left_rotate(p)
                    self.right_rotate(g)

                elif n.parent.left == n and p.parent.right == p:
                    self.right_rotate(p)
                    self.left_rotate(g)

    def insert(self, n):
        y = None
        temp = self.root
        while temp != None:
            y = temp
            if n.data < temp.data:
                temp = temp.left
            else:
                temp = temp.right

        n.parent = y

        if y == None: #newly added node is root
            self.root = n
        elif n.data < y.data:
            y.left = n
        else:
            y.right = n

        self.splay(n)

    def search(self, n, x):
        if x == n.data:
            self.splay(n)
            return n

        elif x < n.data:
            return self.search(n.left, x)
        elif x > n.data:
            return self.search(n.right, x)
        else:
            return None

    def delete(self, n):
        self.splay(n)

        left_subtree = SplayTree()
        left_subtree.root = self.root.left
        if left_subtree.root != None:
            left_subtree.root.parent = None

        right_subtree = SplayTree()
        right_subtree.root = self.root.right
        if right_subtree.root != None:
            right_subtree.root.parent = None

        if left_subtree.root != None:
            m = left_subtree.maximum(left_subtree.root)
            left_subtree.splay(m)
            left_subtree.root.right = right_subtree.root
            self.root = left_subtree.root
            if right_subtree.root != None:
                right_subtree.root.parent = left_subtree.root

        else:
            self.root = right_subtree.root

    def inorder(self, n):
        if n != None:
            self.inorder(n.left)
            print(n.data)
            self.inorder(n.right)

t = SplayTree()

a = Node(10)
b = Node(20)
c = Node(30)
d = Node(100)
e = Node(90)
f = Node(40)
g = Node(50)
h = Node(60)


t.insert(a)

t.insert(b)
t.insert(c)
t.insert(d)
t.insert(e)
t.insert(f)
t.insert(g)
t.insert(h)


print("Tree:")
t.inorder(t.root)
t.delete(d)
print("After Deleting d-100:")
t.inorder(t.root)
t.delete(b)
print("After Deleting b-20:")
t.inorder(t.root)
# output
# Tree:
# 10
# 20
# 30
# 40
# 50
# 60
# 90
# 100
# After Deleting d-100:
# 10
# 20
# 30
# 40
# 50
# 60
# 90
# After Deleting b-20:
# 10
# 30
# 40
# 50
# 60
# 90
    '''
    filename = 'splay.py'
    with open(filename, "w") as f:
        f.write(code)

def bplus():
    code = '''
class Node:
    def __init__(self, leaf=False):
        self.keys = []
        self.child = []
        self.leaf = leaf

    def display(self):
        for i in range(len(self.keys)):
            print(self.keys[i], end=" ")
        print()


class BPlusTree:
    def __init__(self, t):
        self.root = Node(leaf=True)
        self.t = t

    def insert(self, key):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = Node()
            self.root = temp
            temp.child.insert(0, root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, key)
        else:
            self._insert_non_full(root, key)

    def _insert_non_full(self, x, key):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and key < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = key
        else:
            while i >= 0 and key < x.keys[i]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i)
                if key > x.keys[i]:
                    i += 1
            self._insert_non_full(x.child[i], key)

    def _split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = Node(leaf=y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.child = y.child[t: 2 * t]
            y.child = y.child[0: t - 1]

    def display(self):
        self._display(self.root)

    def _display(self, node):
        if node:
            for i in range(len(node.keys)):
                if node.leaf is False:
                    self._display(node.child[i])
                print(node.keys[i], end=" ")
            if node.leaf is False:
                self._display(node.child[len(node.keys)])
        print()


# Test the B+ Tree implementation
tree = BPlusTree(t=3)

# Inserting keys
tree.insert(10)
tree.insert(20)
tree.insert(5)
tree.insert(6)
tree.insert(12)
tree.insert(30)
tree.insert(7)
tree.insert(17)
print("B+ Tree:")
# Displaying the tree
tree.display()
# output:
# B+ Tree:
# 5 6 7 
# 10 12 17 20 30 
    '''
    filename = 'bplus.py'
    with open(filename, "w") as f:
        f.write(code)
def state_space_search():
    code = '''
visited = []
queue = []

def bfs(visited, graph, node):
    visited.append(node)
    queue.append(node)
    while queue:
        m = queue.pop(0)
        for n in graph.get(m, []):  # Check if the node exists in the graph dictionary
            if n not in visited:
                visited.append(n)
                queue.append(n)

def dfs(graph, node, visited):
    if node not in visited:
        visited.append(node)
        for n in graph.get(node, []):  # Check if the node exists in the graph dictionary
            dfs(graph, n, visited)
    return visited

# Get input from the user for the graph
graph = {}
num_nodes = int(input("Enter the number of nodes: "))
for i in range(num_nodes):
    node = input(f"Enter node {i+1}: ")
    edges = input(f"Enter edges for node {i+1} (comma-separated): ")
    if edges.strip() == "":
        graph[node] = []  # Handle the case of no edges for the node
    else:
        graph[node] = edges.split(",")

start_node = input("Enter the starting node for traversal: ")

# Print the graph
print("\nGraph:")
for node, edges in graph.items():
    print(f"{node}: {', '.join(edges)}")

# Perform BFS
visited_bfs = []
bfs(visited_bfs, graph, start_node)
print("\nFollowing is the Breadth-First Search:")
print(visited_bfs)

# Perform DFS
visited_dfs = dfs(graph, start_node, [])
print("\nFollowing is the Depth-First Search:")
print(visited_dfs)


# Output
# Enter the number of nodes: 6
# Enter node 1: 5
# Enter edges for node 1 (comma-separated): 3,7
# Enter node 2: 3
# Enter edges for node 2 (comma-separated): 2,4
# Enter node 3: 7
# Enter edges for node 3 (comma-separated): 8
# Enter node 4: 2
# Enter edges for node 4 (comma-separated): 8
# Enter node 5: 8
# Enter edges for node 5 (comma-separated):
# Enter node 6: 4
# Enter edges for node 6 (comma-separated):

# Enter the starting node for traversal: 5

# Graph:
# 5: 3, 7
# 3: 2, 4
# 7: 8
# 2:
# 4: 8
# 8:

# Following is the Breadth-First Search:
# ['5', '3', '7', '2', '4', '8']

# Following is the Depth-First Search:
# ['5', '3', '2', '4', '8', '7']
    '''
    filename = 'bfsdfs.py'
    with open(filename, "w") as f:
        f.write(code)

def bfstsp():
    code = '''
    
from collections import deque

def tsp_bfs(graph, start):
    n = len(graph) - 1
    queue = deque([(start, [start], 0)])
    min_cost = float('inf')
    min_path = []

    while queue:
        current, path, cost = queue.popleft()

        if len(path) == n:
            cost += graph[current][start]  # Add cost to return to the starting point

            if cost < min_cost:
                min_cost = cost
                min_path = path

        for neighbor in range(1, n + 1):
            if neighbor not in path:
                new_path = path + [neighbor]
                new_cost = cost + graph[current][neighbor]
                queue.append((neighbor, new_path, new_cost))

    return min_path, min_cost

# Get input from the user
n = int(input("Enter the number of cities: "))

# Create an empty graph
graph = [[0] * (n + 1) for _ in range(n + 1)]

# Get the edge weights from the user
print("Enter the edge weights:")
for i in range(1, n + 1):
    for j in range(1, n + 1):
        if i != j:
            graph[i][j] = int(input(f"Edge weight between city {i} and city {j}: "))

start_city = int(input("Enter the starting city: "))

# Solve TSP using BFS
path, cost = tsp_bfs(graph, start_city)

# Print the result
print("Optimal Path:", path)
print("Total Cost:", cost)
#output
# Enter the number of cities: 4
# Enter the edge weights:
# Edge weight between city 1 and city 2: 10
# Edge weight between city 1 and city 3: 15
# Edge weight between city 1 and city 4: 20
# Edge weight between city 2 and city 1: 10
# Edge weight between city 2 and city 3: 35
# Edge weight between city 2 and city 4: 25
# Edge weight between city 3 and city 1: 15
# Edge weight between city 3 and city 2: 35
# Edge weight between city 3 and city 4: 30
# Edge weight between city 4 and city 1: 20
# Edge weight between city 4 and city 2: 25
# Edge weight between city 4 and city 3: 30
# Enter the starting city: 1
# Optimal Path: [1, 2, 4, 3]
# Total Cost: 80

    '''
    filename = 'bfstsp.py'
    with open(filename, "w") as f:
        f.write(code)

def dfstsp():
    code = '''
def tsp_dfs(graph, start_city):
    num_cities = len(graph)
    visited = [False] * num_cities
    path = [start_city]
    min_cost = float('inf')

    def dfs(city, cost):
        nonlocal min_cost

        if len(path) == num_cities:
            cost += graph[city][start_city]
            if cost < min_cost:
                min_cost = cost
                print("Optimal Path:", path)
                print("Optimal Cost:", min_cost)
            return

        visited[city] = True

        for next_city in range(num_cities):
            if not visited[next_city]:
                path.append(next_city + 1)
                dfs(next_city, cost + graph[city][next_city])
                path.pop()

        visited[city] = False

    dfs(start_city - 1, 0)
    return min_cost


# Get the number of cities
num_cities = int(input("Enter the number of cities: "))

# Initialize the adjacency matrix
graph = [[0] * num_cities for _ in range(num_cities)]

# Get the distances between cities from the user
for i in range(num_cities):
    for j in range(num_cities):
        if i != j:
            distance = int(input(f"Enter the distance between city {i+1} and city {j+1}: "))
            graph[i][j] = distance

start_city = int(input("Enter the starting city: "))

# Solve TSP using DFS
optimal_cost = tsp_dfs(graph, start_city)

print("Optimal Cost:", optimal_cost)
output
# Enter the number of cities: 4
# Enter the distance between city 1 and city 2: 10
# Enter the distance between city 1 and city 3: 15
# Enter the distance between city 1 and city 4: 20
# Enter the distance between city 2 and city 1: 10
# Enter the distance between city 2 and city 3: 35
# Enter the distance between city 2 and city 4: 25
# Enter the distance between city 3 and city 1: 15
# Enter the distance between city 3 and city 2: 35
# Enter the distance between city 3 and city 4: 30
# Enter the distance between city 4 and city 1: 20
# Enter the distance between city 4 and city 2: 25
# Enter the distance between city 4 and city 3: 30
# Enter the starting city: 1
# Optimal Path: [1, 2, 3, 4]
# Optimal Cost: 100
# Optimal Path: [1, 3, 4, 2]
# Optimal Cost: 70
# Optimal Cost: 70
'''
    filename = 'dfsstsp.py'
    with open(filename, "w") as f:
        f.write(code)

def closest_pair():
    code = '''
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def closest_pair(points):
    if len(points) == 2:
        return points[0], points[1]
    if len(points) == 1:
        return None

    sorted_points = sorted(points, key=lambda p: p[0])
    mid = len(sorted_points) // 2
    left_closest_pair = closest_pair(sorted_points[:mid])
    right_closest_pair = closest_pair(sorted_points[mid:])

    if left_closest_pair is None:
        min_distance = distance(right_closest_pair[0], right_closest_pair[1])
    elif right_closest_pair is None:
        min_distance = distance(left_closest_pair[0], left_closest_pair[1])
    else:
        min_distance = min(distance(left_closest_pair[0], left_closest_pair[1]), distance(right_closest_pair[0], right_closest_pair[1]))

    closest_across_split = None
    x_mid = sorted_points[mid][0]
    strip = [point for point in sorted_points if abs(point[0] - x_mid) < min_distance]
    strip.sort(key=lambda p: p[1])

    for i in range(len(strip)):
        for j in range(i + 1, min(i + 7, len(strip))):
            current_distance = distance(strip[i], strip[j])
            if current_distance < min_distance:
                min_distance = current_distance
                closest_across_split = strip[i], strip[j]
            print(f"Iteration {i+1}: Closest pair: {closest_across_split}")
            print(f"Iteration {i+1}: Distance: {min_distance}\n")

    if closest_across_split:
        return closest_across_split
    else:
        if left_closest_pair and distance(left_closest_pair[0], left_closest_pair[1]) <= distance(right_closest_pair[0], right_closest_pair[1]):
            return left_closest_pair
        else:
            return right_closest_pair

# Get input from the user
num_points = int(input("Enter the number of points: "))
points = []
for i in range(num_points):
    x = int(input(f"Enter x-coordinate for point {i+1}: "))
    y = int(input(f"Enter y-coordinate for point {i+1}: "))
    points.append((x, y))

# Find the closest pair and print the iterations
closest = closest_pair(points)
p1, p2 = closest

# Print the final closest pair and distance
print(f"\nFinal closest pair: {closest}")
print(f"p1: {p1}")
print(f"p2: {p2}")
print(f"Final distance: {distance(p1,p2)}")
# output
# Enter the number of points: 5
# Enter x-coordinate for point 1: 2
# Enter y-coordinate for point 1: 3
# Enter x-coordinate for point 2: 12
# Enter y-coordinate for point 2: 30
# Enter x-coordinate for point 3: 40
# Enter y-coordinate for point 3: 50
# Enter x-coordinate for point 4: 5
# Enter y-coordinate for point 4: 1
# Enter x-coordinate for point 5: 12
# Enter y-coordinate for point 5: 10
# Iteration 1: Closest pair: ((12, 10), (12, 30))
# Iteration 1: Distance: 20.0

# Iteration 1: Closest pair: ((12, 10), (12, 30))
# Iteration 1: Distance: 20.0

# Iteration 2: Closest pair: ((12, 10), (12, 30))
# Iteration 2: Distance: 20.0

# Iteration 1: Closest pair: None
# Iteration 1: Distance: 3.605551275463989


# Final closest pair: ((2, 3), (5, 1))
# p1: (2, 3)
# p2: (5, 1)
# Final distance: 3.605551275463989

    '''
    filename = 'closestpair.py'
    with open(filename, "w") as f:
        f.write(code)

def huffman():
    code = '''
a=input("Enter characters seperated with space: ").split()  #entering the characters of the word to a list
freq=input("Enter frequency of characters seperated with space: ").split() #entering the frequency of charcaters to a list
b=[int(i) for i in freq]
d=[]
codewords=[]  #a list to store the code words of each character after huffman coding
for i in range(len(a)):
    d.append([a[i],b[i]])
class Node():      #Node for storing the value of each character in terms of frequency
    def __init__(self,val):
        self.val=val
        self.left=None
        self.right=None
        self.huff=None
class Huffman_Tree():    #implementing the huffman tree as a max heap
    def __init__(self):
        self.heap=[Node(i) for i in d]
    def construct_tree(self):  #constructing the tree
        while len(self.heap)>1:
        self.heap.sort(key=lambda x:x.val[1])
        a=self.heap.pop(0)
        b=self.heap.pop(0)
        c=Node(["",a.val[1]+b.val[1]])
        c.left=a
        c.right=b
        a.huff="0"
        b.huff="1"
        self.heap.append(c)
        d=[i.val for i in self.heap]
    def generate_code(self,root,code): #generating the code after the construction of tree
        if root.left==None and root.right==None:
            c=code
            codewords.append([root.val[0],c])
            return
        else:
            c=code
            c=c+root.left.huff
            self.generate_code(root.left,c)
            c=code
            c=c+root.right.huff
            self.generate_code(root.right,c)
p1=Huffman_Tree()
p1.construct_tree()
p1.generate_code(p1.heap[0],"")
cost=0
for i in codewords:
    k=a.index(i[0])
    cost+=b[k]*len(i[1])
print("Average cost per symbol is ",cost) #finding the average cost of huffman code
msg=input("Message to be encoded: ")
code=""
for i in msg:
    for j in codewords:
        if j[0]==i:
            code=code+j[1]
print("The generate code after encoding",msg,"is",code)  #encoding the message based on given codewords
# Output:
# Enter characters seperated with space: A B C D E
# Enter frequency of characters seperated with space: 10 20 40 50 2
# Average cost per symbol is  238
# Message to be encoded: ACED                 
# The generate code after encoding ACED is 10011110000
    '''
    filename = 'huffman.py'
    with open(filename, "w") as f:
        f.write(code)

def kruskals():
    code = '''
class DisjointSet:
    def __init__(self, vertices):
        self.parent = {}
        self.rank = {}
        for v in vertices:
            self.parent[v] = v
            self.rank[v] = 0

    def find(self, v):
        if self.parent[v] != v:
            self.parent[v] = self.find(self.parent[v])
        return self.parent[v]

    def union(self, v1, v2):
        root1 = self.find(v1)
        root2 = self.find(v2)

        if root1 != root2:
            if self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            elif self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1


class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = []

    def add_edge(self, src, dest, weight):
        self.edges.append((src, dest, weight))

    def kruskal_mst(self):
        self.edges = sorted(self.edges, key=lambda x: x[2])  # Sort edges by weight in ascending order
        ds = DisjointSet(self.vertices)
        mst = []
        total_cost = 0

        for edge in self.edges:
            src, dest, weight = edge
            root1 = ds.find(src)
            root2 = ds.find(dest)

            if root1 != root2:
                ds.union(root1, root2)
                mst.append(edge)
                total_cost += weight

        return mst, total_cost


# Get input from the user
num_vertices = int(input("Enter the number of vertices: "))
vertices = [chr(ord('A') + i) for i in range(num_vertices)]
graph = Graph(vertices)

num_edges = int(input("Enter the number of edges: "))
for _ in range(num_edges):
    src, dest, weight = input("Enter source, destination, and weight of an edge (space-separated): ").split()
    graph.add_edge(src, dest, int(weight))

# Find the MST
mst, total_cost = graph.kruskal_mst()

# Print the MST
print("Minimum Spanning Tree:")
for edge in mst:
    print(f"Edge: {edge[0]} - {edge[1]}, Weight: {edge[2]}")

print("Total Cost of MST:", total_cost)
# Output:
# Enter the number of vertices: 5
# Enter the number of edges: 7
# Enter source, destination, and weight of an edge (space-separated): A B 1
# Enter source, destination, and weight of an edge (space-separated): A C 7
# Enter source, destination, and weight of an edge (space-separated): A D 10
# Enter source, destination, and weight of an edge (space-separated): A E 5
# Enter source, destination, and weight of an edge (space-separated): B C 3
# Enter source, destination, and weight of an edge (space-separated): C D 4
# Enter source, destination, and weight of an edge (space-separated): D E 2
# Minimum Spanning Tree:
# Edge: A - B, Weight: 1
# Edge: D - E, Weight: 2
# Edge: B - C, Weight: 3
# Edge: C - D, Weight: 4
# Total Cost of MST: 10
    '''
    filename = 'kruskal.py'
    with open(filename, "w") as f:
        f.write(code)

def binomial():
    code = '''
    
n=int(input("Enter N: "))  #Taking inputs for n and k
k=int(input("Enter K: "))
c=[[0 for i in range(k+1)] for i in range(n+1)]  #creating an array of size n*k
def binomial(n,k):
    if k==0 or k==n:  #returning 1 if k=0 or k=n
        c[n][k]=1
        return c[n][k]
    else:
        if c[n][k]:         #returning the value if present in array to avoid overlapping subproblems
            return c[n][k]
        else:
            c[n][k]=binomial(n-1,k-1)+binomial(n-1,k)    #if not in array, computing the value and storing the value in array for future use
            return c[n][k]
print("answer is",binomial(n,k))
Output:
# Enter N: 5
# Enter K: 2
# answer is 10
    '''
    filename = 'binomial.py'
    with open(filename, "w") as f:
        f.write(code)
def bellman():
    code ='''
class Graph:
    def __init__(self, vertices):
        self.V = vertices + 1
        self.graph = []

    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])

    def printArr(self, dist):
        print("Vertex Distance from Source")
        for i in range(1, self.V):
            print("{0}\t\t{1}".format(i, dist[i]))

    def BellmanFord(self, src):
        dist = [float("Inf")] * self.V
        dist[src] = 0

        for _ in range(self.V - 1):
            for u, v, w in self.graph:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w

        for u, v, w in self.graph:
            if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                print("Graph contains a negative weight cycle")
                return

        self.printArr(dist)


if __name__ == '__main__':
    num_vertices = int(input("Enter the number of vertices: "))
    g = Graph(num_vertices)

    num_edges = int(input("Enter the number of edges: "))

    print("Enter the source, destination, and weight for each edge:")
    for _ in range(num_edges):
        u, v, w = map(int, input().split())
        g.addEdge(u, v, w)

    source = int(input("Enter the source vertex: "))
    g.BellmanFord(source)
    # output
    # Enter the number of vertices: 7
    # Enter the number of edges: 10
    # Enter the source, destination, and weight for each edge:
    # 1 2 6
    # 1 3 5
    # 1 4 5
    # 3 2 -2
    # 4 3 -2
    # 2 5 -1
    # 3 5 1
    # 4 6 -1
    # 5 7 3
    # 6 7 3
    # Enter the source vertex: 1
    # Vertex Distance from Source
    # 1		0
    # 2		1
    # 3		3
    # 4		5
    # 5		0
    # 6		4
    # 7		3
    '''
    filename = 'bellman.py'
    with open(filename, "w") as f:
        f.write(code)

def nqueens():
    code = '''
def is_safe(board, row, col, n):
    # Check if the current position is safe for a queen

    # Check the row on the left side
    for i in range(col):
        if board[row][i] == 1:
            return False

    # Check the upper diagonal on the left side
    i, j = row, col
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    # Check the lower diagonal on the left side
    i, j = row, col
    while i < n and j >= 0:
        if board[i][j] == 1:
            return False
        i += 1
        j -= 1

    return True


def solve_n_queens(n):
    board = [[0 for _ in range(n)] for _ in range(n)]

    def solve_util(col):
        # Base case: If all queens are placed
        if col == n:
            print_solution(board)
            return True

        # Try placing a queen in each row of the current column
        for row in range(n):
            if is_safe(board, row, col, n):
                # Place the queen
                board[row][col] = 1

                # Recur to place the remaining queens
                if solve_util(col + 1):
                    return True

                # Backtrack and remove the queen from the current position
                board[row][col] = 0

        return False

    if not solve_util(0):
        print("No solution exists for the given board size.")

def print_solution(board):
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] == 1:
                print("Q ", end="")
            else:
                print(". ", end="")
        print()
    print()

# Test the program
n = int(input("Enter the number of queens: "))
solve_n_queens(n)
# output:
# Enter the number of queens: 4
# . . Q . 
# Q . . . 
# . . . Q 
# . Q . . 
    '''
    filename = 'nqueens.py'
    with open(filename, "w") as f:
        f.write(code)

def checkqueen():
    code = '''
def is_safe(board, row, col, n):
    # Check if the current position is safe for a queen

    # Check the row on the left side
    for i in range(col):
        if board[row][i] == 1:
            return False

    # Check the upper diagonal on the left side
    i, j = row, col
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    # Check the lower diagonal on the left side
    i, j = row, col
    while i < n and j >= 0:
        if board[i][j] == 1:
            return False
        i += 1
        j -= 1

    return True


def solve_n_queens_util(board, col, n, solutions):
    # Base case: If all queens are placed
    if col == n:
        # Add the current solution to the list of solutions
        solutions.append([row[:] for row in board])
        return

    # Try placing a queen in each row of the current column
    for row in range(n):
        if is_safe(board, row, col, n):
            # Place the queen
            board[row][col] = 1

            # Recur to place the remaining queens
            solve_n_queens_util(board, col + 1, n, solutions)

            # Backtrack and remove the queen from the current position
            board[row][col] = 0


def solve_n_queens(n):
    board = [[0 for _ in range(n)] for _ in range(n)]
    solutions = []

    solve_n_queens_util(board, 0, n, solutions)

    return solutions


def check_queen_safety(solution, row, col):
    # Check if the position is safe
    if solution[row - 1][col - 1] == 1:
        return True
    return False


def print_board(board):
    for row in board:
        print(' '.join(str(cell) for cell in row))


# Test the program
n = int(input("Enter the size of the chessboard: "))

# Generate all possible solutions using backtracking
solutions = solve_n_queens(n)

row = int(input("Enter the row number (1 to {}): ".format(n)))
col = int(input("Enter the column number (1 to {}): ".format(n)))

if row < 1 or row > n or col < 1 or col > n:
    print("Invalid position!")
else:
    queen_safe = False
    for i in range(len(solutions)):
        if check_queen_safety(solutions[i], row, col):
            queen_safe = True
            print("The queen is safe at position ({}, {}).".format(row, col))
            print("Solution:")
            print_board(solutions[i])
            break

    if not queen_safe:
        print("The queen is not safe at position ({}, {}).".format(row, col))
    
    # output:
    # Enter the size of the chessboard: 4
    # Enter the row number (1 to 4): 1
    # Enter the column number (1 to 4): 3
    # The queen is safe at position (1, 3).
    # Solution:
    # 0 0 1 0
    # 1 0 0 0
    # 0 0 0 1
    # 0 1 0 0
    '''
    filename = 'checkqueen.py'
    with open(filename, "w") as f:
        f.write(code)

def hamil():
    code = '''
def hamiltonian_circuit(graph, path):
    for node in graph:
        if node == path[-1]:
            for neighbor in graph[node]:
                if neighbor not in path:
                    if len(path) + 1 == len(graph):
                        path.append(neighbor)
                        print("Hamiltonian circuit has been found and it is", path)
                        return
                    else:
                        new_path = path.copy()
                        new_path.append(neighbor)
                        hamiltonian_circuit(graph, new_path)

# Get graph input from the user
graph = {}
n = int(input("Enter the number of nodes: "))
for i in range(n):
    node = input("Enter node {}: ".format(i+1))
    neighbors = input("Enter neighbors of {}: ".format(node)).split()
    graph[node] = neighbors

# Get initial node input from the user
initial_node = input("Enter the initial node: ")

# Call the function with user inputs
hamiltonian_circuit(graph, [initial_node])
g={"A":["C","B","D"],"B":["A","C","D"],"C":["A","B"],"D":["A","B"]}
output
Enter the number of nodes: 4
Enter node 1: A
Enter neighbors of A: C B D
Enter node 2: B
Enter neighbors of B: A C D
Enter node 3: C
Enter neighbors of C: A B
Enter node 4: D   
Enter neighbors of D: A B
Enter the initial node: A
Hamiltonian circuit has been found and it is ['A', 'C', 'B', 'D']
Hamiltonian circuit has been found and it is ['A', 'D', 'B', 'C']
    '''
    filename = 'hamiltonian.py'
    with open(filename, "w") as f:
        f.write(code)

def stablemarriage():
    code = '''
def stable_marriage(men_preferences, women_preferences):
    engaged = {}
    men_free = list(men_preferences.keys())

    while men_free:
        man = men_free.pop(0)
        preferences = men_preferences[man]
        woman = preferences.pop(0)

        if woman not in engaged:
            engaged[woman] = man
            engaged[man] = woman
        else:
            current_fiance = engaged[woman]
            if women_preferences[woman].index(man) < women_preferences[woman].index(current_fiance):
                engaged[current_fiance] = None
                engaged[woman] = man
                engaged[man] = woman
                men_free.append(current_fiance)
            else:
                men_free.append(man)

    return engaged


# Get preferences from the user
men_preferences = {}
women_preferences = {}

num_men = int(input("Enter the number of men: "))
num_women = int(input("Enter the number of women: "))

for i in range(num_men):
    man = input(f"Enter the name of man {i+1}: ")
    preferences = input(f"Enter the preferences for man {man} (comma-separated): ").split(",")
    men_preferences[man] = preferences

for i in range(num_women):
    woman = input(f"Enter the name of woman {i+1}: ")
    preferences = input(f"Enter the preferences for woman {woman} (comma-separated): ").split(",")
    women_preferences[woman] = preferences


# Find stable matches
matches = stable_marriage(men_preferences, women_preferences)

# Print the matches
for man, woman in matches.items():
    print(f"{man} is engaged to {woman}")
# output:
# Enter the number of men: 3
# Enter the number of women: 3
# Enter the name of man 1: A
# Enter the preferences for man A (comma-separated): X,Y,Z
# Enter the name of man 2: B
# Enter the preferences for man B (comma-separated): Y,X,Z
# Enter the name of man 3: C
# Enter the preferences for man C (comma-separated): X,Y,Z
# Enter the name of woman 1: X
# Enter the preferences for woman X (comma-separated): A,B,C
# Enter the name of woman 2: Y
# Enter the preferences for woman Y (comma-separated): B,A,C
# Enter the name of woman 3: Z
# Enter the preferences for woman Z (comma-separated): A,B,C
# X is engaged to A
# A is engaged to X
# Y is engaged to B
# B is engaged to Y
# Z is engaged to C
# C is engaged to Z
    '''
    filename = 'stablemarriage.py'
    with open(filename, "w") as f:
        f.write(code)

def maxflow():
    code = '''
from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(dict)

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity
        self.graph[v][u] = 0

    def bfs(self, source, sink, parent):
        visited = []
        queue = [(source, float("inf"))]
        visited.append(source)

        while queue:
            u, flow = queue.pop(0)

            for v, capacity in self.graph[u].items():
                if v not in visited and capacity > 0:
                    visited.append(v)
                    parent[v] = (u, capacity)
                    if v == sink:
                        return True

                    queue.append((v, min(flow, capacity)))

        return False

    def ford_fulkerson(self, source, sink):
        max_flow = 0
        parent = {}

        while self.bfs(source, sink, parent):
            path_flow = float("inf")
            v = sink

            while v != source:
                u, capacity = parent[v]
                path_flow = min(path_flow, capacity)
                v = u

            max_flow += path_flow
            v = sink

            while v != source:
                u, _ = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = u

        return max_flow


graph = Graph()

graph.add_edge('A', 'B', 3)
graph.add_edge('A', 'C', 2)
graph.add_edge('B', 'C', 1)
graph.add_edge('B', 'D', 3)
graph.add_edge('C', 'D', 2)
graph.add_edge('D', 'E', 3)

source = 'A'
sink="E"
max_flow = graph.ford_fulkerson(source, sink)

print(f"Maximum Flow: {max_flow}")

#output
# Maximum Flow: 3
    '''
    filename = 'maxflow.py'
    with open(filename, "w") as f:
        f.write(code)

def knapsackbnb():
    code = '''
class Node:
    def __init__(self, level, value, weight, items):
        self.level = level
        self.value = value
        self.weight = weight
        self.items = items

    def __lt__(self, other):
        return self.value > other.value


def knapsack_branch_and_bound(capacity, values, weights):
    n = len(values)
    max_value = 0
    optimal_items = []

    # Sort items by value-to-weight ratio in descending order
    value_weight_ratio = [(values[i] / weights[i], i) for i in range(n)]
    value_weight_ratio.sort(reverse=True)

    # Create a priority queue using a list
    priority_queue = []

    # Create a root node
    root = Node(-1, 0, 0, [])
    priority_queue.append(root)

    while priority_queue:
        # Get the highest priority node from the priority queue
        current_node = max(priority_queue)

        # Remove the current node from the priority queue
        priority_queue.remove(current_node)

        # Check if the current node is promising
        if current_node.level == n - 1:
            continue

        # Create two child nodes
        left_child = Node(current_node.level + 1,
                          current_node.value + values[current_node.level + 1],
                          current_node.weight + weights[current_node.level + 1],
                          current_node.items + [current_node.level + 1])

        right_child = Node(current_node.level + 1,
                           current_node.value,
                           current_node.weight,
                           current_node.items)

        # Check if the left child is feasible and can lead to a better solution
        if left_child.weight <= capacity and left_child.value > max_value:
            max_value = left_child.value
            optimal_items = left_child.items

        # Calculate the upper bound for the right child
        bound = calculate_bound(capacity, n, values, weights, right_child)

        # Check if the right child can lead to a better solution
        if bound > max_value:
            priority_queue.append(right_child)

        # Check if the left child is promising
        if left_child.weight <= capacity and bound > max_value:
            priority_queue.append(left_child)

    return max_value, optimal_items


def calculate_bound(capacity, n, values, weights, node):
    bound = node.value
    total_weight = node.weight
    j = node.level + 1

    while j < n and total_weight + weights[j] <= capacity:
        bound += values[j]
        total_weight += weights[j]
        j += 1

    if j < n:
        bound += (capacity - total_weight) * (values[j] / weights[j])

    return bound


# Get input from the user
n = int(input("Enter the number of items: "))
values = []
weights = []
for i in range(n):
    value = int(input("Enter the value of item {}: ".format(i + 1)))
    weight = int(input("Enter the weight of item {}: ".format(i + 1)))
    values.append(value)
    weights.append(weight)

capacity = int(input("Enter the capacity of the knapsack: "))

max_value, optimal_items = knapsack_branch_and_bound(capacity, values, weights)

print("Maximum value:", max_value)
print("Optimal items:")
for item in optimal_items:
    item_value = values[item]
    item_weight = weights[item]
    print("Item {}: Value = {}, Weight = {}".format(item + 1, item_value, item_weight))

#output
# Enter the number of items: 4
# Enter the value of item 1: 40
# Enter the weight of item 1: 4
# Enter the value of item 2: 42
# Enter the weight of item 2: 7
# Enter the value of item 3: 25
# Enter the weight of item 3: 5
# Enter the value of item 4: 12
# Enter the weight of item 4: 3
# Enter the capacity of the knapsack: 10
# Maximum value: 65
# Optimal items:
# Item 1: Value = 40, Weight = 4
# Item 3: Value = 25, Weight = 5
    '''
    filename = 'knapsackbnb.py'
    with open(filename, "w") as f:
        f.write(code)

def tspbnb():
    code = '''
def tsp_branch_and_bound(graph, starting_city):
    num_cities = len(graph)
    visited = [False] * num_cities
    path = []
    best_path = [starting_city]
    best_cost = float("inf")

    def calculate_bound(path, cost):
        for i in range(num_cities):
            if not visited[i]:
                min_cost = float("inf")
                for j in range(num_cities):
                    if not visited[j] and graph[i][j] < min_cost:
                        min_cost = graph[i][j]
                cost += min_cost
        return cost

    def tsp_helper(curr_city, cost, depth):
        nonlocal best_cost

        path.append(curr_city)
        visited[curr_city] = True

        if depth == num_cities - 1:
            if graph[curr_city][starting_city] != 0 and cost + graph[curr_city][starting_city] < best_cost:
                best_cost = cost + graph[curr_city][starting_city]
                path.append(starting_city)
                best_path[:] = path[:]
                path.pop()
        else:
            bound = calculate_bound(path, cost)
            if bound < best_cost:
                for i in range(num_cities):
                    if not visited[i] and graph[curr_city][i] != 0:
                        tsp_helper(i, cost + graph[curr_city][i], depth + 1)

        path.pop()
        visited[curr_city] = False

    tsp_helper(starting_city, 0, 0)

    return best_path, best_cost


# Getting input from the user
num_cities = int(input("Enter the number of cities: "))
city_distances = []
for i in range(num_cities):
    distances = input(f"Enter the distances from city {i+1} to all other cities separated by spaces: ").split()
    distances = [int(d) for d in distances]
    city_distances.append(distances)

starting_city = int(input("Enter the starting city (1 to N): ")) - 1

# Solving TSP using Branch and Bound
optimal_path, optimal_cost = tsp_branch_and_bound(city_distances, starting_city)

# Printing the optimal tour and its cost
print("Optimal Tour:", "->".join(map(str, optimal_path)))
print("Optimal Cost:", optimal_cost)
#output
# Enter the number of cities: 5
# Enter the distances from city 1 to all other cities separated by spaces: 0 3 1 5 8
# Enter the distances from city 2 to all other cities separated by spaces: 3 0 6 7 9
# Enter the distances from city 3 to all other cities separated by spaces: 1 6 0 4 2
# Enter the distances from city 4 to all other cities separated by spaces: 5 7 4 0 3
# Enter the distances from city 5 to all other cities separated by spaces: 8 9 2 3 0
# Enter the starting city (1 to N): 1
# Optimal Tour: 0->1->3->4->2->0
# Optimal Cost: 16
    '''
def knapsackapprox():
    code = '''
a=[[4,40],[5,25],[7,42],[3,12]]
for i in a:
    i.append(i[1]//i[0])
b=sorted(a,key=lambda x:x[2])
b.reverse()
max1=int(input("enter maximum capacity: "))
weights=[]
item_list=[]
k=int(input("enter parameter: "))
for i in range(k):
    m=int(input("enter item number: "))
    weights.append(b[m-1][0])
    item_list.append(m)
max1-=sum(weights)
i=0
while max1>0 and i<=len(b)-1:
    if b[i][0]<=max1 and (i+1) not in item_list:
        item_list.append(i+1)
        max1=max1-b[i][0]
        i+=1
    else:
        i+=1
print(item_list)
    '''
    filename = 'knapsackapprox.py'
    with open(filename, "w") as f:
        f.write(code)

def tspapprox():
    code ='''

import math

def distance(city1, city2, city_distances):
    return city_distances[city1][city2]

def nearest_neighbor(city_distances, starting_city):
    num_cities = len(city_distances)
    tour = [starting_city]
    remaining_cities = list(range(num_cities))
    remaining_cities.remove(starting_city)
    
    while remaining_cities:
        current_city = tour[-1]
        nearest_city = min(remaining_cities, key=lambda c: distance(current_city, c, city_distances))
        tour.append(nearest_city)
        remaining_cities.remove(nearest_city)
    
    return tour

# Get input from the user
num_cities = int(input("Enter the number of cities: "))
city_distances = []
for i in range(num_cities):
    distances = input(f"Enter the distances from city {i+1} to all other cities separated by spaces: ").split()
    distances = [int(d) for d in distances]
    city_distances.append(distances)

starting_city = int(input("Enter the starting city (1 to N): ")) - 1

# Solve TSP using nearest neighbor heuristic
tour = nearest_neighbor(city_distances, starting_city)
total_distance = sum(distance(tour[i], tour[i+1], city_distances) for i in range(len(tour)-1))
total_distance += distance(tour[-1], tour[0], city_distances)

# Adjust tour and starting_city index for printing
tour = [city + 1 for city in tour]
starting_city += 1

# Print the result
print("Tour:", tour)
print("Total distance:", total_distance)    
'''
    filename = 'tspapprox.py'
    with open(filename, "w") as f:
        f.write(code)

def maxnoparrallel():
    code = '''
import multiprocessing

def find_maximum(numbers):
    return max(numbers)

if __name__ == '__main__':
    numbers = input("Enter a list of numbers (separated by spaces): ").split()
    numbers = [int(num) for num in numbers]

    num_processes = multiprocessing.cpu_count()
    chunk_size = len(numbers) // num_processes
    chunk_size = max(chunk_size, 1)
    chunks = [numbers[i:i+chunk_size] for i in range(0, len(numbers), chunk_size)]

    pool = multiprocessing.Pool(processes=num_processes)
    results = pool.map(find_maximum, chunks)
    overall_max = max(results)

    pool.close()
    pool.join()

    print("Maximum number:", overall_max)
    # Output:
    # Enter a list of numbers (separated by spaces): 5 10 15 20 25 30 45 89 69 22
    # Maximum number: 89
    
    '''
    filename = 'maxnoparallel.py'
    with open(filename, "w") as f:
        f.write(code)

def minnoparallel():
    code = '''
import multiprocessing

def find_minimum(numbers):
    return min(numbers)

if __name__ == '__main__':
    numbers = input("Enter a list of numbers (separated by spaces): ").split()
    numbers = [int(num) for num in numbers]

    num_processes = multiprocessing.cpu_count()
    chunk_size = len(numbers) // num_processes
    chunk_size = max(chunk_size, 1)
    chunks = [numbers[i:i+chunk_size] for i in range(0, len(numbers), chunk_size)]

    pool = multiprocessing.Pool(processes=num_processes)
    results = pool.map(find_minimum, chunks)
    overall_min = min(results)

    pool.close()
    pool.join()

    print("Minimum number:", overall_min)
    # Output:
    # Enter a list of numbers (separated by spaces): 5 10 15 20 25 30 45 89 69 22
    # Minimum number: 5
    '''
    filename = 'mixnnoparallel.py'
    with open(filename, "w") as f:
        f.write(code)
def randomizedselect_and_sort():
    code = '''
import random

def partition(arr, low, high):
    pivot_index = random.randint(low, high)
    arr[high], arr[pivot_index] = arr[pivot_index], arr[high]
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quickselect(arr, low, high, k):
    if low == high:
        return arr[low]

    pivot_index = partition(arr, low, high)

    if k == pivot_index:
        return arr[k]
    elif k < pivot_index:
        return quickselect(arr, low, pivot_index - 1, k)
    else:
        return quickselect(arr, pivot_index + 1, high, k)

def quicksort(arr, low, high):
    if low < high:
        pivot_index = partition(arr, low, high)
        quicksort(arr, low, pivot_index - 1)
        quicksort(arr, pivot_index + 1, high)

# Get input from the user
numbers = input("Enter a list of numbers (separated by spaces): ").split()
numbers = [int(num) for num in numbers]

k = int(input("Enter the value of k for quickselect: "))

# Find the kth smallest element using quickselect
result = quickselect(numbers, 0, len(numbers) - 1, k)
print(f"The {k}th smallest element is: {result}")

# Sort the list using quicksort
quicksort(numbers, 0, len(numbers) - 1)
print("Sorted list:", numbers)
#output
Enter a list of numbers (separated by spaces): 8 5 4 3 2 1 7 8 18 22
Enter the value of k for quickselect: 5
The 5th smallest element is: 7
Sorted list: [1, 2, 3, 4, 5, 7, 8, 8, 18, 22]
    '''
    filename = 'randomizedselect_and_sort.py'
    with open(filename, "w") as f:
        f.write(code)

def eightpuzzle():
    code='''
import copy
from heapq import heappush, heappop

n = 3

row = [1, 0, -1, 0]  # Represents the movement in rows: bottom, left, top, right
col = [0, -1, 0, 1]  # Represents the movement in columns: bottom, left, top, right

class priorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, k):
        heappush(self.heap, k)

    def pop(self):
        return heappop(self.heap)

    def empty(self):
        return not self.heap

class node:
    def __init__(self, parent, mat, empty_tile_pos, cost, level):
        self.parent = parent  # Parent node
        self.mat = mat  # Current matrix state
        self.empty_tile_pos = empty_tile_pos  # Position of the empty tile
        self.cost = cost  # Number of misplaced tiles (heuristic)
        self.level = level  # Number of moves made so far

    def __lt__(self, nxt):
        return self.cost < nxt.cost

def calculateCost(mat, final):
    count = 0
    for i in range(n):
        for j in range(n):
            if mat[i][j] and mat[i][j] != final[i][j]:
                count += 1
    return count

def newNode(mat, empty_tile_pos, new_empty_tile_pos, level, parent, final):
    new_mat = copy.deepcopy(mat)
    x1, y1 = empty_tile_pos
    x2, y2 = new_empty_tile_pos
    new_mat[x1][y1], new_mat[x2][y2] = new_mat[x2][y2], new_mat[x1][y1]
    cost = calculateCost(new_mat, final)
    new_node = node(parent, new_mat, new_empty_tile_pos, cost, level)
    return new_node

def printMatrix(mat):
    for i in range(n):
        for j in range(n):
            print("%d " % mat[i][j], end=" ")
        print()

def isSafe(x, y):
    return x >= 0 and x < n and y >= 0 and y < n

def printPath(root):
    if root == None:
        return
    printPath(root.parent)
    printMatrix(root.mat)
    print()

def solve(initial, empty_tile_pos, final):
    pq = priorityQueue()
    cost = calculateCost(initial, final)
    root = node(None, initial, empty_tile_pos, cost, 0)
    pq.push(root)

    while not pq.empty():
        minimum = pq.pop()

        if minimum.cost == 0:  # If the minimum node is the goal state
            printPath(minimum)  # Print the path from root to destination
            return

        for i in range(4):  # Generate all possible children by moving the empty tile
            new_tile_pos = [
                minimum.empty_tile_pos[0] + row[i],
                minimum.empty_tile_pos[1] + col[i],
            ]

            if isSafe(new_tile_pos[0], new_tile_pos[1]):
                child = newNode(
                    minimum.mat,
                    minimum.empty_tile_pos,
                    new_tile_pos,
                    minimum.level + 1,
                    minimum,
                    final,
                )
                pq.push(child)  # Add the child to the priority queue for further exploration

initial = [[1, 2, 3],
            [5, 6, 0],
            [7, 8, 4]]

final = [[1, 2, 3],
         [5, 8, 6],
         [0, 7, 4]]

empty_tile_pos = [1, 2]

solve(initial, empty_tile_pos, final)
#output
# 1  2  3  
# 5  6  0  
# 7  8  4  

# 1  2  3  
# 5  0  6  
# 7  8  4  

# 1  2  3  
# 5  8  6  
# 7  0  4  

# 1  2  3  
# 5  8  6  
# 0  7  4  
    '''
    filename = 'eightpuzzle.py'
    with open(filename, "w") as f:
        f.write(code)

def display_menu():
    print("Welcome to the Python Function Menu!")
    print("1. splay")
    print("2. bplus")
    print("3. state_space_search")
    print("4. bfstsp")
    print("5. dfstsp")
    print("6. closest_pair")
    print("7. huffman")
    print("8. kruskals")
    print("9. binomial")
    print("10. bellman")
    print("11. nqueens")
    print("12. checkqueen")
    print("13. hamil")
    print("14. stablemarriage")
    print("15. maxflow")
    print("16. knapsackbnb")
    print("17. tspbnb")
    print("18. knapsackapprox")
    print("19. tspapprox")
    print("20. maxnoparallel")
    print("21. minnoparallel")
    print("22. randomizedselect_and_sort")
    print("23. eightpuzzle")

    while True:
        try:
            choice = int(input("Enter the number of the function you want to execute (or 0 to exit): "))
            if choice == 0:
                print("Exiting the menu...")
                break
            elif choice == 1:
                splay()
            elif choice == 2:
                bplus()
            elif choice == 3:
                state_space_search()
            elif choice == 4:
                bfstsp()
            elif choice == 5:
                dfstsp()
            elif choice == 6:
                closest_pair()
            elif choice == 7:
                huffman()
            elif choice == 8:
                kruskals()
            elif choice == 9:
                binomial()
            elif choice == 10:
                bellman()
            elif choice == 11:
                nqueens()
            elif choice == 12:
                checkqueen()
            elif choice == 13:
                hamil()
            elif choice == 14:
                stablemarriage()
            elif choice == 15:
                maxflow()
            elif choice == 16:
                knapsackbnb()
            elif choice == 17:
                tspbnb()
            elif choice == 18:
                knapsackapprox()
            elif choice == 19:
                tspapprox()
            elif choice == 20:
                maxnoparrallel()
            elif choice == 21:
                minnoparallel()
            elif choice == 22:
                randomizedselect_and_sort()
            elif choice == 23:
                eightpuzzle()
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
