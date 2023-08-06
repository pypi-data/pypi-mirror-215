def splay():
    code = '''
    
    '''
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
def bellamn():
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
    