# Depth-first-search and Breadth-first-search algorithms applied to a maze

## What is Depth-first-search?
Depth-first search (DFS) is an algorithm for traversing or searching tree or graph data structures. The algorithm starts at the root node (selecting some arbitrary node as the root node in the case of a graph) and explores as far as possible along each branch before backtracking. Extra memory, usually a stack, is needed to keep track of the nodes discovered so far along a specified branch which helps in backtracking of the graph.

The time and space analysis of DFS differs according to its application area. In theoretical computer science, DFS is typically used to traverse an entire graph, and takes time O(|V| + |E|) where |V| is the number of vertices and |E| the number of edges. This is linear in the size of the graph. In these applications it also uses space O(|V|) in the worst case to store the stack of vertices on the current search path as well as the set of already-visited vertices

## What is Breadth-first-search?
Breadth-first search (BFS) is an algorithm for searching a tree data structure for a node that satisfies a given property. It starts at the tree root and explores all nodes at the present depth prior to moving on to the nodes at the next depth level. Extra memory, usually a queue, is needed to keep track of the child nodes that were encountered but not yet explored.

The time complexity can be expressed as O(|V|+|E|), since every vertex and every edge will be explored in the worst case. 
|V| is the number of vertices and |E| is the number of edges in the graph. Note that O(|E|) may vary between O(1) and O(|V|^{2}), depending on how sparse the input graph is.

## How this implementation works
Once the code is launched, a window with the maze will pop up: from this clicking any free square with the left button of the mouse will set the start and node goal. To reset the start/end nodes, just right click on them. Once the start and end nodes are chosen, pressing the key space button will open a window through which the algorithm to use can be chosen: DFS algorithm only shows a visualization of the nodes visited to reach the goal node, without returning a path whereas BFS also shows the retrieved path.
The start node is going to be displayed in Blue, the end node in Orange, visited nodes in red, nodes in the queue in green, the final retrieved path in purple.
Once the algorithm is finished, it is possible to re-initialize a maze just by pressing "*r*" key.