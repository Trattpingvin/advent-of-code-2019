class Node():
	def __init__(self):
		self.parent = None
		self.children = []

def buildGraph(filename='inputs/day6.txt'):
	graph = {}
	with open(filename) as f:
		for line in f:
			parent_string, child_string = line.strip().split(')')
			if parent_string in graph:
				parent = graph[parent_string]
			else:
				parent = Node()
				graph[parent_string] = parent
			if child_string in graph:
				child = graph[child_string]
			else:
				child = Node()
				graph[child_string] = child

			child.parent = parent
			parent.children.append(child)
	return graph

def traverse(node, depth):
	score = depth
	for child in node.children:
		score += traverse(child, depth+1)
	return score


def solvepart1():
	graph = buildGraph()
	root = graph['COM']
	ans = traverse(root, 0)
	return ans

def shortest_path(graph, src, dst):
	#basically dijsktra from wikipedia
	dist = {}
	Q = set()
	import math
	for node in graph:
		node = graph[node]
		dist[node] = math.inf
		Q.add(node)
	dist[src] = 0

	while len(Q) > 0:
		shortest_node = None
		shortest_dist = math.inf
		for node in Q:
			if dist[node] < shortest_dist:
				shortest_dist = dist[node]
				shortest_node = node
		Q.remove(shortest_node)
		
		if shortest_node==dst:
			return dist[shortest_node]
		
		
		for node in shortest_node.children + [shortest_node.parent]:
			if node:#ignore root
				current_dist = dist[shortest_node] + 1
				if current_dist < dist[node]:
					dist[node] = current_dist

	return False



def solvepart2():
	graph = buildGraph()
	ans = shortest_path(graph, graph['YOU'], graph['SAN']) - 2
	return ans

if __name__=='__main__':
	print(solvepart1())
	print(solvepart2())

